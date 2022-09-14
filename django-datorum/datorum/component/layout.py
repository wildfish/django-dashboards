import logging
from dataclasses import dataclass
from typing import Dict, Optional

from django.template import Context, Template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


logger = logging.getLogger(__name__)


def css_template(width: int, css_classes: list):
    return f"span-{width} {css_classes}"


class LayoutBase:
    template_name: Optional[str] = None
    css_classes: Optional[str] = None
    width: Optional[int] = 6
    image_url: Optional[str] = None

    def __init__(
        self, *layout_components, css_classes=None, width=None, image_url=None
    ):
        if not layout_components:
            layout_components = []

        self.layout_components = layout_components

        if css_classes:
            self.css_classes = css_classes

        if width:
            self.width = width

        if image_url:
            self.image_url = image_url

    def get_components_rendered(self, dashboard, context: Dict) -> str:
        html = ""
        dashboard_components = dict([(x.key, x) for x in dashboard.get_components()])

        for layout_component in self.layout_components:
            dashboard_component = None

            # if str, we want the final dashboard_component
            if isinstance(layout_component, str):
                dashboard_component = dashboard_components.get(layout_component)

            if hasattr(layout_component, "render"):
                html += layout_component.render(dashboard, context)
            elif dashboard_component:
                html += str(dashboard_component)

        return mark_safe(html)


class ComponentLayout(LayoutBase):
    """
    holder for the components in the layout
    """

    def render(self, dashboard, context: Dict):
        return self.get_components_rendered(dashboard, context)


class HTMLComponentLayout(ComponentLayout):
    """
    template wrapper for components
    """

    def render(self, dashboard, context: Dict, **kwargs) -> str:
        components = self.get_components_rendered(dashboard, context)
        request = context.get("request")
        component_context = {
            "components": components,
            "css": css_template(self.width, self.css_classes),
        }

        return render_to_string(
            self.template_name, context=component_context, request=request
        )


class Card(HTMLComponentLayout):
    template_name: str = "datorum/layout/components/card.html"
    css_classes: str = "dashboard-component"


class Div(HTMLComponentLayout):
    template_name: str = "datorum/layout/components/div.html"


class TabContainer(HTMLComponentLayout):
    template_name: str = "datorum/layout/components/tabs/container.html"
    css_classes: str = "tab-content"

    def render(self, dashboard, context: Dict, **kwargs) -> str:
        tab_panels = self.get_components_rendered(dashboard, context)
        # make tab links for each tab
        links = "".join(tab.render_link() for tab in self.layout_components)

        request = context.get("request")
        component_context = {
            "css": css_template(self.width, self.css_classes),
            "links": links,
            "tab_panels": tab_panels,
            "first": self.layout_components[0],
        }

        html = render_to_string(
            self.template_name, context=component_context, request=request
        )
        return mark_safe(html)


class Tab(HTMLComponentLayout):
    tab_label: str = ""
    template_name: str = "datorum/layout/components/tabs/component.html"
    css_classes: str = "tab-pane fade"

    def render_link(self):
        return mark_safe(
            render_to_string(
                "datorum/layout/components/tabs/link.html",
                {
                    "link": self.tab_label,
                },
            )
        )

    def render(self, dashboard, context: Dict, **kwargs):
        return super().render(dashboard, context, **kwargs)


@dataclass
class HTML:
    html: str
    width: Optional[int] = 6

    def render(self, dashboard, context: Dict, **kwargs):
        to_render = f'<div class="{css_template(self.width, [])}">{self.html}</div>'
        return Template(to_render).render(Context(context))


@dataclass
class HR(HTML):
    html: str = "<hr />"


@dataclass
class Header(HTML):
    html: str = ""
    heading: str = ""
    size: int = 1

    def __post_init__(self):
        self.html = f"<h{self.size}>{self.heading}</h{self.size}>"
