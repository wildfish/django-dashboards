from django import template
from django.template import RequestContext

from datorum.component import Component
from datorum.types import ValueData


register = template.Library()


@register.simple_tag(takes_context=True)
def render(context: RequestContext, component: Component) -> ValueData:
    """Render a component, passing request"""
    return component.for_render(request=context["request"])
