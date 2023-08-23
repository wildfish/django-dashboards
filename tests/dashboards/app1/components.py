from dataclasses import dataclass

from django.template import Context

from dashboards.component import Component


@dataclass
class TextAsHTML(Component):
    def render_as_html(self, context: Context):
        return f"<i>{context['rendered_value']}</i>"


@dataclass
class ComponentNoRender(Component):
    """
    A component that can't be rendered and will raise a Runtime
    """

    pass
