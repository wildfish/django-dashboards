import copy
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

from django.template import Context, Template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from .. import config
from . import CTA


CARD_CLASSES: Dict[str, str] = {
    "card": "card",
    "header": "card-header",
    "image": "card-img",
    "body": "card-body",
    "footer": "card-footer",
}

TAB_CONTAINER_CLASSES: Dict[str, str] = {
    "tab_container": "tab-container",
    "tabs": "tabs",
    "tab_content": "tab-content",
}

TAB_CLASSES: Dict[str, str] = {
    "tab": "tab",
    "tab_link": "",
}

DIV_CLASSES: Dict[str, str] = {"wrapper": ""}


DEFAULT_LAYOUT_COMPONENT_CLASSES: Dict[str, Dict[str, str]] = {
    "Card": CARD_CLASSES,
    "TabContainer": TAB_CONTAINER_CLASSES,
    "Tab": TAB_CLASSES,
    "Div": DIV_CLASSES,
}


def css_template(*css_classes):
    css = " ".join(filter(None, css_classes))
    return f"{css}"


class LayoutBase:
    template_name: Optional[str] = None
    css_classes: Optional[Union[str, Dict[str, str]]] = None
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

        self.component_css = self.get_component_css(css_classes)

        if grid_css_classes:
            self.grid_css_classes = grid_css_classes
        else:
            self.grid_css_classes = config.Config().DASHBOARDS_DEFAULT_GRID_CSS

        self.component_context = {}
        for k, v in kwargs.items():
            self.component_context[k] = v

    def get_component_css(self, custom_css_classes):
        # set to default initially
        component_css = copy.copy(self.css_classes)

        # update css classes if they have been passed in
        if custom_css_classes:
            # convert component_css to dict to match
            if isinstance(custom_css_classes, dict):
                component_css = component_css or {}

            # need to be a dict so we can update keys
            if isinstance(component_css, dict) and isinstance(custom_css_classes, dict):
                component_css.update(custom_css_classes)
            else:
                component_css = custom_css_classes

        return component_css

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
                "css": css_template(self.grid_css_classes),
                "component_css": self.component_css,
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
    template_name: str = "dashboards/layout/components/card.html"
    css_classes: Optional[
        Dict[str, str]
    ] = config.Config().DASHBOARDS_LAYOUT_COMPONENT_CLASSES["Card"]

    def __init__(
        self,
        *layout_components,
        heading: Optional[str] = None,
        footer: Optional[str] = None,
        image_url: Optional[str] = None,
        actions: Optional[List[tuple]] = None,
        **kwargs,
    ):
        super().__init__(*layout_components, **kwargs)
        # add additional attributes to component_context
        self.component_context["heading"] = heading
        self.component_context["footer"] = footer
        self.component_context["image_url"] = image_url
        self.component_context["actions"] = actions or []

    def get_component_css(self, custom_css_classes):
        # legacy fix. make sure custom_css_classes is a dict as this is what card template requires
        if custom_css_classes and isinstance(custom_css_classes, str):
            # if sting assume this is the card wrapper class
            custom_css_classes = {"card": custom_css_classes}

        return super().get_component_css(custom_css_classes)

    def render(self, dashboard, context: Context, **kwargs) -> str:
        # convert CTA to a url
        for i, action in enumerate(self.component_context["actions"]):
            if isinstance(action[0], CTA):
                self.component_context["actions"][i] = (
                    action[0].get_href(obj=dashboard.object),
                    action[1],
                )

        return super().render(dashboard, context, **kwargs)


class Div(HTMLComponentLayout):
    template_name: str = "dashboards/layout/components/div.html"
    css_classes: Optional[
        Dict[str, str]
    ] = config.Config().DASHBOARDS_LAYOUT_COMPONENT_CLASSES["Div"]


class TabContainer(HTMLComponentLayout):
    template_name: str = "dashboards/layout/components/tabs/container.html"
    css_classes: Optional[
        Dict[str, str]
    ] = config.Config().DASHBOARDS_LAYOUT_COMPONENT_CLASSES["TabContainer"]

    def render(self, dashboard, context: Context, **kwargs) -> str:
        tab_panels = self.get_components_rendered(dashboard, context)
        # make tab links for each tab
        tabs = "".join(tab.render_tab() for tab in self.layout_components)

        request = context.get("request")
        component_context = super().get_component_context()
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
    template_name: str = "dashboards/layout/components/tabs/content.html"
    css_classes: Optional[
        Dict[str, str]
    ] = config.Config().DASHBOARDS_LAYOUT_COMPONENT_CLASSES["Tab"]

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
                "dashboards/layout/components/tabs/tab.html",
                {
                    "tab_label": self.tab_label,
                    "tab_css_classes": self.component_context.get(
                        "component_css", {}
                    ).get("tab"),
                    "link_css_classes": self.component_context.get(
                        "component_css", {}
                    ).get("tab_link"),
                },
            )
        )


@dataclass
class HTML:
    html: str

    def render(self, *args, context: Context, **kwargs):
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
