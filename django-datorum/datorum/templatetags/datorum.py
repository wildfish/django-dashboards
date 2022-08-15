from typing import Optional

from django import template
from django.forms import Form
from django.template import RequestContext

from datorum.component import Component
from datorum.types import ValueData


register = template.Library()


@register.simple_tag(takes_context=True)
def render(context: RequestContext, component: Component) -> ValueData:
    """Render a component, passing request"""
    return component.for_render(request=context["request"])


@register.simple_tag(takes_context=True)
def get_filter_form(context: RequestContext, component: Component) -> Optional[Form]:
    """Render a component, passing request"""
    if component.filter_form:
        return component.filter_form(request=context["request"])
    return None
