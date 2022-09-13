import logging
from typing import Dict

from django.template import Context, Template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

logger = logging.getLogger(__name__)


class ComponentHolder:
    def __init__(self, *components):
        self.components = list(components)

    def get_components_rendered(self, dashboard, context: Dict):
        html = ""
        components = dict([(x.key, x) for x in dashboard.get_components()])

        for component in self.components:
            # layout component
            if hasattr(component, "render"):
                html += component.render(dashboard, context)
            else:
                # dashboard components
                try:
                    c = components[component]
                    html += str(c)
                except KeyError:
                    logger.warning(f"component {component} not found")
                    continue

        return mark_safe(html)


class LayoutComponent(ComponentHolder):
    """
    holder for the components in the layout
    """

    def render(self, dashboard, context: Dict):
        return self.get_components_rendered(dashboard, context)


class HTMLComponent(ComponentHolder):
    """
    template wrapper for components
    """

    template_name: str
    css_class_names: str = ""

    def __init__(self, *components, element_id: str, css_class_names: str = ""):
        self.element_id = element_id
        self.css_class_names += f" {css_class_names}"
        super().__init__(*components)

    def render(self, dashboard, context: Dict, **kwargs):
        components = self.get_components_rendered(dashboard, context)
        request = context.get("request")
        component_context = {
            "components": components,
            "css_class": self.css_class_names,
            "element_id": self.element_id,
        }

        return render_to_string(
            self.template_name, context=component_context, request=request
        )


class Card(HTMLComponent):
    template_name: str = "datorum/layout/components/card.html"
    css_class_names: str = "card"

    def __init__(
        self,
        *components,
        element_id: str,
        image_url: str = None,
        css_class_names: str = "",
    ):
        self.image_url = image_url
        super().__init__(
            *components, element_id=element_id, css_class_names=css_class_names
        )


class Div(HTMLComponent):
    template_name: str = "datorum/layout/components/div.html"
    css_class_names: str = "div"


class TabContainer(HTMLComponent):
    template_name: str = "datorum/layout/components/tabs/container.html"
    css_class_names: str = "tab-content"

    def render(self, dashboard, context: Dict, **kwargs):
        tab_panels = self.get_components_rendered(dashboard, context)
        # make tab links for each tab
        links = "".join(tab.render_link() for tab in self.components)

        request = context.get("request")
        component_context = {
            "css_class": self.css_class_names,
            "element_id": self.element_id,
            "links": links,
            "tab_panels": tab_panels,
            "first": self.components[0],
        }

        html = render_to_string(
            self.template_name, context=component_context, request=request
        )
        return mark_safe(html)


class Tab(HTMLComponent):
    template_name: str = "datorum/layout/components/tabs/component.html"
    css_class_names: str = "tab-pane fade"

    def __init__(
        self,
        tab_label,
        *components,
        element_id: str,
        css_class_names: str = "",
    ):
        super().__init__(
            *components, element_id=element_id, css_class_names=css_class_names
        )
        self.tab_label = tab_label

    def render_link(self):
        return mark_safe(
            render_to_string(
                "datorum/layout/components/tabs/link.html",
                {
                    "element_id": self.element_id,
                    "link": self.tab_label,
                },
            )
        )

    def render(self, dashboard, context: Dict, **kwargs):
        return super().render(dashboard, context, **kwargs)


class HTML:
    def __init__(self, html):
        self.html: str = html

    def render(self, dashboard, context: Dict, **kwargs):
        return Template(str(self.html)).render(Context(context))


class HR(HTML):
    def __init__(self):
        self.html = "<hr />"


class Header(HTML):
    def __init__(self, heading: str, size: int = 1):
        self.html = f"<h{size}>{heading}</h{size}>"
