from typing import Optional

from django import template
from django.forms import Form
from django.template import RequestContext

from datorum.component import Component
from datorum.dashboard import Dashboard


register = template.Library()


@register.simple_tag(takes_context=True)
def render_component(context: RequestContext, component: Component, htmx: bool):
    return component.render(context=context, htmx=htmx, call_deferred=not htmx)


@register.simple_tag(takes_context=True)
def render_dashboard(context: RequestContext, dashboard: Dashboard):
    request = context["request"]
    return dashboard.render(request=request, template_name=dashboard.template_name)


@register.filter()
def next_grid_area(gen):
    return next(gen)
