import inspect
import itertools
import logging
import string
from typing import List, Optional

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe

from datorum import config
from datorum.component import Component
from datorum.exceptions import ComponentNotFoundError
from datorum.layout import LayoutComponent
from datorum.permissions import BasePermission
from datorum.registry import registry


logger = logging.getLogger(__name__)


class DashboardRenderMixin:
    template_name: str = "datorum/layout/grid.html"

    class Layout:
        """
        Components classes to define layout

        components = LayoutComponent(
            Div(
                Div(
                    "a",
                    "b",
                    c="text_group_div",
                    element_id="div_1",
                ),
                Div(
                    "d",
                    "e",
                    "f",
                    element_id="div_2",
                ),
                element_id="div_wrapper",
            ),
            'g',
            'h'
        )
        """

        components: Optional[LayoutComponent] = None

    def get_context(self):
        context = {"dashboard": self}
        return context

    def render(self, request: HttpRequest, template_name=None):
        context = self.get_context()
        context["request"] = request

        layout = self.Layout
        if layout.components:
            context["call_deferred"] = False
            return layout.components.render(dashboard=self, context=context)

        if not template_name:
            template_name = self.template_name

        return mark_safe(render_to_string(template_name, context))

    @staticmethod
    def grid_areas():
        for i in itertools.count(1):
            for p in itertools.product(string.ascii_lowercase, repeat=i):
                yield "".join(p)


class DashboardType(type):
    def __new__(mcs, cls, bases, attrs):
        dashboard_class = super().__new__(mcs, cls, bases, attrs)
        registry.register(dashboard_class)
        return dashboard_class


class Dashboard(DashboardRenderMixin, metaclass=DashboardType):
    include_in_graphql: bool = True
    permission_classes: Optional[List[BasePermission]] = None

    def __init__(self, **kwargs):
        self._components_cache = {}
        super().__init__()

    def get_context(self):
        context = super().get_context()
        context["components"] = self.get_components()
        return context

    @classmethod
    def get_attributes_order(cls):
        """
        Get the order of the attributes as they are defined on the Dashboard class.
        Follows mro, then reverses to parents first.
        """
        attributes_to_class = []
        attributes_to_class.extend(
            [list(vars(bc).keys()) for bc in cls.__mro__ if issubclass(bc, Dashboard)]
        )
        attributes_to_class.sort(reverse=True)
        return [a for nested in attributes_to_class for a in nested]

    @classmethod
    def get_components(cls) -> list[Component]:
        attributes = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a)))

        components_to_keys = {}
        awaiting_dependents = {}
        for key, component in attributes:
            if isinstance(component, Component):
                component.dashboard_class = cls.__name__
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

        components = list(components_to_keys.values())
        components.sort(key=lambda c: cls.get_attributes_order().index(c.key))

        return components

    def get_dashboard_permissions(self):
        """
        Returns a list of permissions attached to a dashboard.
        """
        if self.permission_classes:
            permissions_classes = self.permission_classes
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

    def has_permissions(self, request: HttpRequest) -> bool:
        """
        Check if the request should be permitted.
        Raises exception if the request is not permitted.
        """
        for permission in self.get_dashboard_permissions():
            if not permission.has_permission(request):
                return False
        return True

    def get_urls(self):
        from django.template.defaultfilters import slugify
        from django.urls import path

        from .views import DashboardView

        name = slugify(self.__class__.__name__)
        return [
            path(
                "%s/" % name,
                DashboardView.as_view(dashboard_class=self.__class__),
                name="%s_dashboard" % name,
            ),
        ]

    @property
    def urls(self):
        urls = self.get_urls()
        return urls

    class Meta:
        name: str

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
