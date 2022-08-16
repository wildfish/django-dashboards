from django.template import Template


def render_component_test(context, htmx):
    template_to_render = Template(
        f"{{% load datorum %}}{{% render_component component=component htmx={htmx} %}}"
    )
    return template_to_render.render(context)
