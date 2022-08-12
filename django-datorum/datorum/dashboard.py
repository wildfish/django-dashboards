import inspect
import logging
from copy import deepcopy

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from datorum.component import Component


logger = logging.getLogger(__name__)


class DashboardRenderMixin:
    class Layout:
        """
        Components works a like fields/formsets on contrib forms. e.g

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


class Dashboard(DashboardRenderMixin):
    def __init__(self, request: HttpRequest):
        self.request = request

    def get_context(self):
        return {"components": self.get_components(), "request": self.request}

    @classmethod
    def get_components(cls, with_layout=True) -> list[Component]:
        attributes = inspect.getmembers(cls, lambda a: not (inspect.isroutine(a)))
        components = []

        for key, component in attributes:
            if isinstance(component, Component):
                if not component.key:
                    component.key = key
                if not component.render_type:
                    component.render_type = component.__class__.__name__
                components.append(component)

        if with_layout:
            components = cls.apply_layout(components=deepcopy(components))

        return components

    class Meta:
        name: str
