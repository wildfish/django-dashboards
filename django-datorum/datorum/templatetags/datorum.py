from typing import Optional

from django import template
from django.forms import Form
from django.template import RequestContext

from datorum.component import Component
from datorum.dashboard import Dashboard


register = template.Library()


@register.inclusion_tag("datorum/components/component.html", takes_context=True)
def render_component(context: RequestContext, component: Component, htmx: bool):
    request = context["request"]
    rendered_value = component.for_render(request=request)
    return {
        "request": context["request"],
        "component": component,
        "htmx": htmx,
        "rendered_value": rendered_value,
    }


@register.simple_tag(takes_context=True)
def get_filter_form(context: RequestContext, component: Component) -> Optional[Form]:
    """Render a component, passing request"""
    if component.filter_form:
        return component.filter_form(request=context["request"])
    return None


@register.simple_tag(takes_context=True)
def render_dashboard(context: RequestContext, dashboard: Dashboard, as_div: bool = False):
    request = context["request"]
    return dashboard.as_div(request=request) if as_div else dashboard.render(request=request)
