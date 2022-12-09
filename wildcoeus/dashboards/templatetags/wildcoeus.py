import random

from django import template
from django.template import RequestContext

from wildcoeus.dashboards.component import Component
from wildcoeus.dashboards.dashboard import Dashboard
from wildcoeus.dashboards.registry import registry


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
    return dashboard.render(request=request, template_name=dashboard.Meta.template_name)


@register.simple_tag()
def dashboard_urls(app_label):
    """
    Get top level dashboards (not model/object ones) for an app label
    """
    return {
        d._meta.name: d.get_absolute_url()
        for d in registry.get_by_app_label(app_label)
        if not d._meta.model and d._meta.include_in_menu
    }


@register.filter(name="lookup")
def lookup(value, arg):
    return value.get(arg)


@register.filter
def cta_href(cta, obj):
    return cta.get_href(obj=obj)
