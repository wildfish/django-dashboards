from typing import Any, Dict, List, Optional, Type

from django.apps import apps
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template import Context
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from wildcoeus.dashboards.component import Component
from wildcoeus.dashboards.component.layout import Card, ComponentLayout
from wildcoeus.dashboards.config import Config
from wildcoeus.dashboards.log import logger
from wildcoeus.dashboards.permissions import BasePermission


class DashboardType(type):
    def __new__(mcs, name, bases, attrs):
        # Collect components from current class and remove them from attrs.
        attrs["components"] = {
            key: attrs.pop(key)
            for key, value in list(attrs.items())
            if isinstance(value, Component)
        }

        dashboard_class = super().__new__(mcs, name, bases, attrs)
        components = {}
        for base in reversed(dashboard_class.__mro__):
            # Collect components from base class.
            if hasattr(base, "components"):
                components.update(base.components)

            # Field shadowing.
            for attr, value in base.__dict__.items():
                if value is None and attr in components:
                    components.pop(attr)

        # add components to class.
        dashboard_class.components = components

        module = attrs.pop("__module__")
        attr_meta = attrs.get("Meta", None)
        meta = attr_meta or getattr(dashboard_class, "Meta", None)
        base_meta = getattr(dashboard_class, "_meta", None)
        dashboard_class._meta = meta

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
            if not hasattr(meta, "name"):
                dashboard_class._meta.name = name
            if not hasattr(meta, "model"):
                dashboard_class._meta.model = base_meta.model
            if not hasattr(meta, "lookup_kwarg"):
                dashboard_class._meta.lookup_kwarg = base_meta.lookup_kwarg
            if not hasattr(meta, "lookup_field"):
                dashboard_class._meta.lookup_field = base_meta.lookup_field
            if not hasattr(meta, "include_in_graphql"):
                dashboard_class._meta.include_in_graphql = base_meta.include_in_graphql
            if not hasattr(meta, "include_in_menu"):
                dashboard_class._meta.include_in_menu = base_meta.include_in_menu
            if not hasattr(meta, "permission_classes"):
                dashboard_class._meta.permission_classes = base_meta.permission_classes
            if not hasattr(meta, "template_name"):
                dashboard_class._meta.template_name = base_meta.template_name

        return dashboard_class


class Dashboard(metaclass=DashboardType):
    _meta: Type["Dashboard.Meta"]
    components: Dict[str, Any]

    def __init__(self, *args, **kwargs):
        logger.debug(f"Calling init for {self.class_name()}")
        self.kwargs = kwargs
        # set component value/defer to be method calls to get_FOO_value, get_FOO_refer if defined on dashboard
        for key, component in self.components.items():
            if hasattr(self, f"get_{key}_value"):
                logger.debug(f"setting component value to 'get_{key}_value' for {key}")
                component.value = getattr(self, f"get_{key}_value")

            elif hasattr(self, f"get_{key}_defer"):
                logger.debug(f"setting component defer to 'get_{key}_defer' for {key}")
                component.defer = getattr(self, f"get_{key}_defer")

            if (
                component.value is None
                and component.defer is None
                and component.defer_url is None
            ):
                logger.warning(f"component {key} has no value or defer set.")

    class Meta:
        name: str
        include_in_graphql: bool = True
        include_in_menu: bool = True
        permission_classes: Optional[List[BasePermission]] = None
        template_name: Optional[str] = None
        model = None
        lookup_kwarg: str = "lookup"  # url parameter name
        lookup_field: str = "pk"  # model field

    class Layout:
        components: Optional[ComponentLayout] = None

    @classmethod
    def class_name(cls):
        return str(cls.__name__).lower()

    @classmethod
    def get_slug(cls):
        return f"{slugify(cls._meta.app_label)}_{slugify(cls.__name__)}"

    @classmethod
    def get_components(cls) -> list[Component]:
        components_to_keys = {}
        awaiting_dependents = {}
        for key, component in cls.components.items():
            if not component.dashboard:
                component.dashboard = cls
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
        if cls.Meta.permission_classes:
            permissions_classes = cls.Meta.permission_classes
        else:
            permissions_classes = []
            for permission_class_path in Config().WILDCOEUS_DEFAULT_PERMISSION_CLASSES:
                try:
                    permissions_class = import_string(permission_class_path)
                    permissions_classes.append(permissions_class)
                except ModuleNotFoundError:  # pragma: no cover
                    logger.warning(
                        f"{permission_class_path} is invalid permissions path"
                    )

        return [permission() for permission in permissions_classes]

    @classmethod
    def has_permissions(cls, request: HttpRequest, handle: bool = True):
        """
        Check if the request should be permitted.
        Raises exception if the request is not permitted.
        """
        for permission in cls.get_dashboard_permissions():
            if not permission.has_permission(request):
                if handle:
                    return permission.handle_no_permission(request)
                else:
                    return False
        return True

    @classmethod
    def get_urls(cls):
        from django.urls import path

        from .views import DashboardView

        name = cls.class_name()

        return [
            path(
                f"{cls._meta.app_label}/{name}/",
                DashboardView.as_view(dashboard_class=cls),
                name=cls.get_slug(),
            ),
        ]

    @classmethod
    def urls(cls):
        urls = cls.get_urls()
        return urls

    @classmethod
    def get_absolute_url(cls):
        return reverse(f"wildcoeus.dashboards:dashboards:{cls.get_slug()}")

    def get_context(self) -> dict:
        return {"dashboard": self, "components": self.get_components()}

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
                *[Card(k, **_get_layout(c)) for k, c in self.components.items()]
            )

        context["call_deferred"] = False
        return layout.components.render(dashboard=self, context=Context(context))

    def __str__(self):
        return self.Meta.name


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
            f"wildcoeus.dashboards:dashboards:{self.get_slug()}_dashboard_detail",
            kwargs={self._meta.lookup_kwarg: self.object.pk},
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

    @classmethod
    def get_urls(cls):
        from django.urls import path

        from .views import DashboardView

        name = cls.class_name()

        return [
            path(
                f"{cls._meta.app_label}/{name}/<str:{cls._meta.lookup_kwarg}>/",
                DashboardView.as_view(dashboard_class=cls),
                name=f"{cls.get_slug()}_dashboard_detail",
            ),
        ]
