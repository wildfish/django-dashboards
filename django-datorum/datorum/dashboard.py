import inspect
import logging
from copy import deepcopy

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from datorum import permissions
from datorum.component import Component
from datorum.registry import registry


logger = logging.getLogger(__name__)

# todo: move to a default settings when available
DEFAULT_PERMISSION_CLASSES = [permissions.AllowAny]


class DashboardRenderMixin:
    class Layout:
        """
        Components works a like fields/formsets on contrib forms. e.g.

        components = {
            "group_one": {
                "components": ["a", "b", "c"],
                "component_widths": [3, 6],
                "group_width": 6,
            },
            "group_two": {
                "components": ["d", "e"],
                "group_width": 3,
                # no component_widths so will default to first component.width or Layout.default_component_width
            },
            # None can be uses as a catch all for the remaining non grouped ones.
            None: {
                "components": ["calculated_example", "chart_example"],
            }
        }

        """

        components: dict = {}
        default_component_width: int = 4

    def get_context(self):
        raise NotImplementedError(
            "Subclasses of DashboardRenderMixin must provide a get_context() method."
        )

    def render(self, template_name=None, layout_context=None):
        context = self.get_context()
        context.update(layout_context)
        return mark_safe(render_to_string(template_name, context))

    __str__ = render
    __html__ = render

    def as_div(self):
        """Render as <div> components."""
        return self.render("datorum/layout/div.html", {"layout": self.Layout()})

    def as_grid(self):
        """Render as <div> grid components."""
        return self.render("datorum/layout/grid.html", {"layout": self.Layout()})

    @classmethod
    def apply_layout(cls, components: list[Component]) -> list[Component]:
        """
        If a fixed layout has been defined, order, group and annotate components as needed for rendering.
        Otherwise return as per the attribute order.
        """
        layout = cls.Layout
        width = layout.default_component_width

        # if we have a defined layout, fields not in this layout are not added/shown.
        components_with_layout = []
        if layout.components:
            components_to_keys = {c.key: c for c in components}
            for group, attrs in layout.components.items():
                for i, key in enumerate(attrs.get("components")):
                    component = components_to_keys.get(key)
                    if component:
                        try:
                            component.width = attrs.get("component_widths", [])[i]
                        except IndexError:
                            logger.debug(f"Missing component_widths for {key} at {i}")
                            if not component.width:  # if not set directly on component
                                component.width = width

                        component.group_width = attrs.get("group_width")
                        component.group = attrs.get("group", group)
                        components_with_layout.append(component)
                    else:
                        logger.warning(f"Missing component for {key}")

        # default layout
        else:
            for component in components:
                if not component.width:
                    component.width = width
                components_with_layout.append(component)

        return components_with_layout


class DashboardMetaClass(type):
    def __new__(cls, clsname, bases, attrs):
        newclass = super().__new__(cls, clsname, bases, attrs)
        registry.register(newclass)
        return newclass


class Dashboard(DashboardRenderMixin, metaclass=DashboardMetaClass):
    permission_classes = DEFAULT_PERMISSION_CLASSES

    def __init__(self, request: HttpRequest = None):
        self.request = request

    def get_context(self):
        return {"components": self.get_components(), "request": self.request}

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
    def get_components(cls, with_layout=True) -> list[Component]:
        attributes = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a)))

        components_to_keys = {}
        awaiting_dependents = {}
        for key, component in attributes:
            if isinstance(component, Component):
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

        if with_layout:
            components = cls.apply_layout(components=deepcopy(components))

        return components

    class Meta:
        name: str
