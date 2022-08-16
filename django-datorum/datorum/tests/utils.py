from django.template import Template


def render_component_test(context, htmx):
    template_to_render = Template(
        """
        {% load datorum %}
        {% render_component component=component htmx=False %}
    """
    )
    print(template_to_render.render(context))
    return template_to_render.render(context)
