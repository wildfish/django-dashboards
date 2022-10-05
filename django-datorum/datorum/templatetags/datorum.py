from django import template
from django.template import RequestContext

from datorum.component import Component
from datorum.dashboard import Dashboard
from datorum.registry import registry


register = template.Library()


@register.simple_tag(takes_context=True)
def render_component(context: RequestContext, component: Component, htmx: bool):
    return component.render(context=context, htmx=htmx, call_deferred=not htmx)


@register.simple_tag(takes_context=True)
def render_dashboard(context: RequestContext, dashboard: Dashboard):
    request = context["request"]
    return dashboard.render(request=request, template_name=dashboard.template_name)


@register.simple_tag()
def dashboards_for_app(app_label):
    """
    Get top level dashboards (not model/object ones) for an app label
    """
    return [d for d in registry.get_by_app_label(app_label) if not d._meta.model]
