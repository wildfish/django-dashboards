from django.template import Template


def render_component_test(context, htmx):
    template_to_render = Template(
        f"{{% load wildcoeus %}}{{% render_component component=component htmx={htmx} %}}"
    )
    return template_to_render.render(context)


def render_dashboard_test(context):
    template_to_render = Template(
        "{% load wildcoeus %}}{{% render_dashboard dashboard=dashboard %}"
    )
    return template_to_render.render(context)
