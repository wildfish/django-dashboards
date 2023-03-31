import random
from typing import Dict, List, Type, Union, cast

from django import template
from django.template import RequestContext

from dashboards.component import Component
from dashboards.dashboard import Dashboard
from dashboards.menus.menu import DashboardMenuItem, Menu, MenuItem
from dashboards.menus.registry import menu_registry
from dashboards.registry import registry


register = template.Library()


@register.simple_tag()
def random_ms_delay(a: int = 0, b: int = 200):
    return f"{random.randint(a, b)}ms"


@register.simple_tag(takes_context=True)
def render_component(context: RequestContext, component: Component, htmx: bool):
    return component.render(context=context, htmx=htmx, call_deferred=not htmx)


@register.simple_tag(takes_context=True)
def render_dashboard(context: RequestContext, dashboard: Dashboard):
    request = context["request"]
    return dashboard.render(
        # TODO: for some reason mypy complains about this one line
        request=request,
        template_name=dashboard._meta.template_name,  # type: ignore
    )


@register.simple_tag()
def dashboard_urls(app_label):
    """
    Get top level dashboards (not model/object ones) for an app label
    """
    return {
        d._meta.name: d.get_absolute_url()
        for d in registry.get_by_app_label(app_label)
        if not getattr(d._meta, "model", None) and d._meta.include_in_menu
    }


@register.filter()
def lookup(value, arg):
    return value.get(arg)


@register.filter
def cta_href(cta, obj):
    return cta.get_href(obj=obj)


@register.tag(name="dashboard_menus")
def do_dashboard_menus(parser, token):
    return DashboardMenuNode()


class DashboardMenuNode(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        request = context.get("request")
        sections: Dict[str, List[Union["MenuItem", "DashboardMenuItem"]]] = {}
        active_section = None  # section which has the current page in it

        if request:
            dashboard = context.get("dashboard")
            context_object = None

            if dashboard:
                context_object = getattr(dashboard, "object")

            # find and load menus from registry
            menu_registry.autodiscover()

            menus = cast(List[Type[Menu]], menu_registry.items)
            for menu in menus:
                sections.setdefault(menu.name, [])
                for menu_item in menu.render(request, context_object):
                    sections[menu.name].append(menu_item)
                    # only do the first one found
                    if active_section is None and menu_item.selected or menu_item.open:
                        active_section = menu.name

        context["sections"] = sections
        context["active_section"] = active_section
        return ""
