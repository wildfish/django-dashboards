import inspect
import logging
from typing import List, Optional

from django.apps import apps
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template import Context
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from datorum import config
from datorum.component import Component
from datorum.component.layout import Card, ComponentLayout
from datorum.exceptions import ComponentNotFoundError
from datorum.permissions import BasePermission


logger = logging.getLogger(__name__)


class DashboardType(type):
    def __new__(mcs, name, bases, attrs):
        dashboard_class = super().__new__(mcs, name, bases, attrs)
        module = attrs.pop("__module__")
        attr_meta = attrs.get("Meta", None)
        meta = attr_meta or getattr(dashboard_class, "Meta", None)
        base_meta = getattr(dashboard_class, "_meta", None)
        setattr(dashboard_class, "_meta", meta)
        if getattr(meta, "app_label", None) is None:
            # Look for an application configuration to attach the model to.
            app_config = apps.get_containing_app_config(module)

            if app_config is None:
                if name not in (
                    "ModelDashboard",
                    "Dashboard",
                ):  # TODO needs better way to exclude the base class?

                    raise RuntimeError(
                        "Model class %s.%s doesn't declare an explicit "
                        "app_label and isn't in an application in "
                        "INSTALLED_APPS." % (module, name)
                    )
            else:
                dashboard_class._meta.app_label = app_config.label

        if base_meta:
            if not hasattr(meta, "model"):
                dashboard_class._meta.model = base_meta.model
            if not hasattr(meta, "lookup_kwarg"):
                dashboard_class._meta.lookup_kwarg = base_meta.lookup_kwarg
            if not hasattr(meta, "lookup_field"):
                dashboard_class._meta.lookup_field = base_meta.lookup_field

        return dashboard_class


class Dashboard(metaclass=DashboardType):
    include_in_graphql: bool = True
    permission_classes: Optional[List[BasePermission]] = None
    template_name: Optional[str] = None

    def __init__(self, **kwargs):
        self._components_cache = {}
        self.kwargs = kwargs
        super().__init__()

    def get_slug(self):
        return f"{slugify(self._meta.app_label)}_{slugify(self.__class__.__name__)}"

    def get_context(self) -> dict:
        return {"dashboard": self, "components": self.get_components()}

    @classmethod
    def get_attributes_order(cls):
        """
        Get the order of the attributes as they are defined on the Dashboard class.
        Follows mro, then reverses to parents first.
        """
        attributes_to_class = []
        attributes_to_class.extend(
            [list(vars(bc).keys()) for bc in cls.mro() if issubclass(bc, Dashboard)]
        )
        attributes_to_class.sort(reverse=True)
        return [a for nested in attributes_to_class for a in nested]

    @classmethod
    def get_component_attributes(cls):
        attributes = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a)))
        components = [(k, c) for k, c in attributes if isinstance(c, Component)]
        components.sort(key=lambda t: cls.get_attributes_order().index(t[0]))
        return components

    def get_components(self) -> list[Component]:
        component_attributes = self.get_component_attributes()

        components_to_keys = {}
        awaiting_dependents = {}
        for key, component in component_attributes:
            if not component.dashboard:
                component.dashboard = self
            if not component.key:
                component.key = key
            if not component.render_type:
                component.render_type = component.__class__.__name__
            components_to_keys[key] = component

            if component.dependents:
                awaiting_dependents[key] = component.dependents

        for component, dependents in awaiting_dependents.items():
            components_to_keys[component].dependent_components = [
                components_to_keys.get(d) for d in dependents  # type: ignore
            ]

        return list(components_to_keys.values())

    @classmethod
    def get_dashboard_permissions(cls):
        """
        Returns a list of permissions attached to a dashboard.
        """
        if cls.permission_classes:
            permissions_classes = cls.permission_classes
        else:
            permissions_classes = []
            for (
                permission_class_path
            ) in config.Config().DATORUM_DEFAULT_PERMISSION_CLASSES:
                try:
                    permissions_class = import_string(permission_class_path)
                    permissions_classes.append(permissions_class)
                except ModuleNotFoundError:
                    logger.warning(
                        f"{permission_class_path} is invalid permissions path"
                    )

        return [permission() for permission in permissions_classes]

    @classmethod
    def has_permissions(cls, request: HttpRequest) -> bool:
        """
        Check if the request should be permitted.
        Raises exception if the request is not permitted.
        """
        for permission in cls.get_dashboard_permissions():
            if not permission.has_permission(request):
                return False
        return True

    def get_urls(self):
        from django.urls import path

        from .views import DashboardView

        name = str(self.__class__.__name__).lower()

        return [
            path(
                f"{self._meta.app_label}/{name}/",
                DashboardView.as_view(dashboard_class=self.__class__),
                name=self.get_slug(),
            ),
        ]

    @property
    def urls(self):
        urls = self.get_urls()
        return urls

    def get_absolute_url(self):
        return reverse(f"datorum:dashboards:{self.get_slug()}")

    class Meta:
        model = None
        name: str
        lookup_kwarg: str = "lookup"  # url parameter name
        lookup_field: str = "pk"  # model field

    class Layout:
        """
        Components classes to define layout

        components = ComponentLayout(
            Div(
                Div(
                    "a",
                    "b",
                    c="text_group_div",
                ),
                Div(
                    "d",
                    "e",
                    "f",
                ),
            ),
            'g',
            'h'
        )
        """

        components: Optional[ComponentLayout] = None

    def render(self, request: HttpRequest, template_name=None):
        """
        Renders 3 ways
        - if template is provided - use custom template
        - else if layout is set use layout.
        - else render a generic layout by wrapping all components.
        """
        context = self.get_context()
        context["request"] = request

        layout = self.Layout()

        # Render with template
        if template_name:
            return mark_safe(render_to_string(template_name, context))

        # No layout, so create default one, copying any LayoutOptions elements from the component to the card
        # TODO Card as the default should be an option
        # TODO make width/css_classes generic, for now tho we don't need template.
        if not layout.components:

            def _get_layout(c: Component) -> dict:
                return {
                    "width": c.width,
                    "css_classes": f"{c.css_classes if c.css_classes else ''} {Card.css_classes}",
                }

            layout.components = ComponentLayout(
                *[Card(k, **_get_layout(c)) for k, c in self.get_component_attributes()]
            )

        context["call_deferred"] = False
        return layout.components.render(dashboard=self, context=Context(context))

    def __str__(self):
        return self.Meta.name

    def __getitem__(self, name):
        # see if this is a component
        if not self._components_cache:  # do we have a cache?
            components = dict([(x.key, x) for x in self.get_components()])
            self._components_cache.update(components)

        # is it a component
        try:
            value = self._components_cache[name]
        except KeyError:
            try:
                value = getattr(self, name)
            except AttributeError:
                raise ComponentNotFoundError

        return value


class ModelDashboard(Dashboard):
    @property
    def object(self):
        return self.get_object()

    def get_queryset(self):
        if self._meta.model is None:
            raise AttributeError("model is not set on Meta")

        return self._meta.model.objects.all()

    def get_absolute_url(self):
        return reverse(
            f"datorum:dashboards:{self.get_slug()}", kwargs={"pk": self.object.pk}
        )

    def get_object(self):
        """
        Get django object based on lookup params
        """
        qs = self.get_queryset()

        if self._meta.lookup_kwarg not in self.kwargs:
            raise AttributeError(f"{self._meta.lookup_kwarg} not in kwargs")

        lookup = self.kwargs[self._meta.lookup_kwarg]

        return get_object_or_404(qs, **{self._meta.lookup_field: lookup})

    def get_urls(self):
        from django.urls import path

        from .views import DashboardView

        name = str(self.__class__.__name__).lower()

        return [
            path(
                f"{self._meta.app_label}/{name}/<str:{self._meta.lookup_kwarg}>/",
                DashboardView.as_view(dashboard_class=self.__class__),
                name=f"{self.get_slug()}_dashboard_detail",
            ),
        ]
