from typing import Optional

from django import template
from django.forms import Form
from django.template import RequestContext

from datorum.component import Component
from datorum.dashboard import Dashboard


register = template.Library()


@register.simple_tag(takes_context=True)
def render_component(context: RequestContext, component: Component, htmx: bool):
    render_context = {}
    render_context["request"] = context["request"]
    render_context["htmx"] = htmx
    render_context["call_deferred"] = not htmx

    return component.render(**render_context)


@register.simple_tag(takes_context=True)
def get_filter_form(context: RequestContext, component: Component) -> Optional[Form]:
    """Render a component, passing request"""
    if component.filter_form:
        return component.filter_form(request=context["request"])
    return None


@register.simple_tag(takes_context=True)
def render_dashboard(context: RequestContext, dashboard: Dashboard):
    request = context["request"]
    return dashboard.render(request=request, template_name=dashboard.template_name)


@register.filter()
def next_grid_area(gen):
    return next(gen)
