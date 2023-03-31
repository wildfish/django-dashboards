from typing import Any, ClassVar, Dict, List, Optional

from django.db.models import Model
from django.http import HttpRequest
from django.template import Context
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from dashboards.component import Component
from dashboards.component.layout import Card, ComponentLayout
from dashboards.config import Config
from dashboards.log import logger
from dashboards.meta import ClassWithAppConfigMeta
from dashboards.permissions import BasePermission
from dashboards.registry import Registrable


class Dashboard(Registrable, ClassWithAppConfigMeta):
    components: Dict[str, Any]

    class Meta(ClassWithAppConfigMeta.Meta):
        abstract = True
        include_in_menu: ClassVar[bool]
        permission_classes: Optional[List[BasePermission]] = None
        template_name: Optional[str] = None
        lookup_kwarg: str = "lookup"  # url parameter name
        lookup_field: str = "pk"  # model field

    def __init__(self, *args, **kwargs):
        logger.debug(f"Calling init for {self.class_name()}")
        self.object = None
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

    @classmethod
    def postprocess_meta(cls, class_meta, resolved_meta_class):
        # add default includes based on the abstract status
        if not hasattr(class_meta, "include_in_menu"):
            resolved_meta_class.include_in_menu = not resolved_meta_class.abstract

        # collect all the components from all the base classes
        cls.components = {}
        for base in reversed(cls.__bases__):
            if not hasattr(base, "components") or not isinstance(base.components, dict):  # type: ignore
                continue

            for k, v in (
                (k, v) for k, v in base.components.items() if isinstance(v, Component)  # type: ignore
            ):
                cls.components[k] = v

        # add all components from the current class
        for k, v in (
            (k, v) for k, v in cls.__dict__.items() if isinstance(v, Component)
        ):
            cls.components[k] = v

        return super().postprocess_meta(class_meta, resolved_meta_class)

    class Layout:
        components: Optional[ComponentLayout] = None

    @classmethod
    def class_name(cls):
        return str(cls.__name__).lower()

    @classmethod
    def get_slug(cls):
        return f"{slugify(cls._meta.app_label)}_{slugify(cls.__name__)}"

    @classmethod
    def get_id(cls):
        return cls.get_slug()

    def get_components(self) -> list[Component]:
        components_to_keys = {}
        awaiting_dependents = {}
        for key, component in self.components.items():
            component.object = self.object
            if not component.dashboard:
                component.dashboard = self.__class__
            if not component.key:
                component.key = key
            if not component.verbose_name:
                component.verbose_name = key
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
        if cls._meta.permission_classes:
            permission_classes = cls._meta.permission_classes
        else:
            permission_classes = []
            for permission_class_path in Config().DASHBOARDS_DEFAULT_PERMISSION_CLASSES:
                try:
                    permission_class = import_string(permission_class_path)
                    permission_classes.append(permission_class)
                except ModuleNotFoundError:  # pragma: no cover
                    logger.warning(
                        f"{permission_class_path} is invalid permissions path"
                    )

        return [permission() for permission in permission_classes]

    @classmethod
    def has_permissions(cls, request: HttpRequest, handle: bool = True):
        """
        Check if the request should be permitted.
        Raises exception if the request is not permitted.
        """
        for permission in cls.get_dashboard_permissions():
            if not permission.has_permission(request=request, dashboard=cls):
                if handle:
                    return permission.handle_no_permission(
                        request=request, dashboard=cls
                    )
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
        return reverse(f"dashboards:{cls.get_slug()}")

    def get_context(self, **kwargs) -> dict:
        return kwargs

    def render(self, request: HttpRequest, template_name=None):
        """
        Renders 3 ways
        - if template is provided - use custom template
        - else if layout is set use layout.
        - else render a generic layout by wrapping all components.
        """
        context = self.get_context(request=request, call_deferred=False)

        layout = self.Layout()

        # Render with template
        if template_name:
            # set required attributes on each component
            self.get_components()
            # add dashboard to the context so it's available for the template
            context["dashboard"] = self
            return mark_safe(render_to_string(template_name, context))

        # No layout, so create default one, copying any LayoutOptions elements from the component to the card
        # TODO Card as the default should be an option
        # TODO make width/css_classes generic, for now tho we don't need template.
        if not layout.components:

            def _get_layout(c: Component) -> dict:
                return {
                    "grid_css_classes": c.grid_css_classes,
                    "css_classes": c.css_classes or "",
                }

            layout.components = ComponentLayout(
                *[Card(k, **_get_layout(c)) for k, c in self.components.items()]
            )

        return layout.components.render(dashboard=self, context=Context(context))

    def __str__(self):
        return self._meta.name


class ModelDashboard(Dashboard):
    object: Model

    class Meta(Dashboard.Meta):
        model: ClassVar[Model]
        abstract = True

    def __init__(self, *args, **kwargs):
        super(ModelDashboard, self).__init__(*args, **kwargs)
        self.object = kwargs.get("object")
        if not self.object:
            self.object = self.get_object(**kwargs)

    def get_queryset(self):
        if self._meta.model is None:
            raise AttributeError("model is not set on Meta")

        return self._meta.model.objects.all()

    def get_absolute_url(self):
        return reverse(
            f"dashboards:{self.get_slug()}_detail",
            kwargs={self._meta.lookup_kwarg: self.object.pk},
        )

    def get_object(self, **kwargs):
        """
        Get django object based on lookup params
        """
        qs = self.get_queryset()

        if self._meta.lookup_kwarg not in kwargs:
            raise AttributeError(f"{self._meta.lookup_kwarg} not in kwargs")

        lookup = kwargs[self._meta.lookup_kwarg]

        return qs.get(**{self._meta.lookup_field: lookup})

    @classmethod
    def get_urls(cls):
        from django.urls import path

        from .views import DashboardView

        name = cls.class_name()

        return [
            path(
                f"{cls._meta.app_label}/{name}/<str:{cls._meta.lookup_kwarg}>/",
                DashboardView.as_view(dashboard_class=cls),
                name=f"{cls.get_slug()}_detail",
            ),
        ]
