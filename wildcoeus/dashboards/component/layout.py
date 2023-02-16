from dataclasses import dataclass
from typing import Any, List, Optional, Tuple

from django.template import Context, Template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from .. import config


def css_template(*css_classes):
    css = " ".join(filter(None, css_classes))
    return f"{css}"


class LayoutBase:
    template_name: Optional[str] = None
    css_classes: Optional[str] = None
    grid_css_classes: Optional[str] = None
    layout_components: Tuple[Any, ...]

    def __init__(
        self,
        *layout_components,
        css_classes=None,
        grid_css_classes=None,
        **kwargs,
    ):
        self.layout_components = layout_components or ()

        if css_classes:
            self.css_classes = css_classes

        if grid_css_classes:
            self.grid_css_classes = grid_css_classes
        else:
            self.grid_css_classes = config.Config().WILDCOEUS_DEFAULT_GRID_CSS

        self.component_context = {}
        for k, v in kwargs.items():
            self.component_context[k] = v

    def get_components_rendered(self, dashboard, context: Context) -> str:
        html = ""
        dashboard_components = dict([(x.key, x) for x in dashboard.get_components()])

        for layout_component in self.layout_components:
            dashboard_component = None

            # if str, we want the final dashboard_component
            if isinstance(layout_component, str):
                dashboard_component = dashboard_components.get(layout_component)

            if hasattr(layout_component, "render"):
                html += layout_component.render(dashboard=dashboard, context=context)
            elif dashboard_component:
                html += dashboard_component.render(context=context)

        return mark_safe(html)


class ComponentLayout(LayoutBase):
    """
    holder for the components in the layout

    include_default: sets anything not show to be shown via the default, it's only applied here at top level.
    """

    def render(self, dashboard, context: Context):
        return self.get_components_rendered(dashboard=dashboard, context=context)


class HTMLComponentLayout(ComponentLayout):
    """
    template wrapper for components
    """

    def get_component_context(self):
        component_context = self.component_context
        component_context.update(
            {
                "css": css_template(self.grid_css_classes, self.css_classes),
            }
        )

        return component_context

    def render(self, dashboard, context: Context, **kwargs) -> str:
        request = context.get("request")
        components = self.get_components_rendered(dashboard=dashboard, context=context)
        component_context = self.get_component_context()
        component_context.update(
            {
                "components": components,
            }
        )

        return render_to_string(
            self.template_name, context=component_context, request=request
        )


class Card(HTMLComponentLayout):
    template_name: str = "wildcoeus/dashboards/layout/components/card.html"
    css_classes: str = "dashboard-component"
    heading: Optional[str] = None
    footer: Optional[str] = None
    image_url: Optional[str] = None
    actions: Optional[List[tuple]] = None

    def get_component_context(self):
        """split the passed in css from the layout css"""
        component_context = self.component_context
        component_context.update(
            {"css": css_template(self.grid_css_classes), "card_css": self.css_classes}
        )

        return component_context


class Div(HTMLComponentLayout):
    template_name: str = "wildcoeus/dashboards/layout/components/div.html"


class TabContainer(HTMLComponentLayout):
    template_name: str = "wildcoeus/dashboards/layout/components/tabs/container.html"
    css_classes: str = "tab-container"
    tab_list_classes: str = "tabs"

    def render(self, dashboard, context: Context, **kwargs) -> str:
        tab_panels = self.get_components_rendered(dashboard, context)
        # make tab links for each tab
        tabs = "".join(tab.render_tab() for tab in self.layout_components)

        request = context.get("request")
        component_context = self.get_component_context()
        component_context.update(
            {
                "tabs": tabs,
                "tab_panels": tab_panels,
                "first": self.layout_components[0],
            }
        )

        html = render_to_string(
            self.template_name, context=component_context, request=request
        )
        return mark_safe(html)


class Tab(HTMLComponentLayout):
    tab_label: str = ""
    template_name: str = "wildcoeus/dashboards/layout/components/tabs/content.html"
    css_classes: str = "tab-content"
    li_css_classes: str = ""
    link_css_classes: str = ""

    def __init__(self, tab_label, *layout_components, **kwargs):
        self.tab_label = tab_label
        super().__init__(*layout_components, **kwargs)

    def get_component_context(self):
        component_context = super().get_component_context()
        component_context.update({"layout_component": self})

        return component_context

    def render_tab(self):
        return mark_safe(
            render_to_string(
                "wildcoeus/dashboards/layout/components/tabs/tab.html",
                {
                    "tab_label": self.tab_label,
                    "li_css_classes": self.component_context.get("li_css_classes"),
                    "link_css_classes": self.component_context.get("link_css_classes"),
                },
            )
        )


@dataclass
class HTML:
    html: str

    def render(self, dashboard, context: Context, **kwargs):
        to_render = f"{self.html}"
        return Template(to_render).render(context=Context(context))


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
