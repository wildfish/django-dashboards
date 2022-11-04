from django.template import Context

import pytest

from tests.utils import render_component_test
from wildcoeus.dashboards.component import CTA, Chart, Stat, Table, Text
from wildcoeus.dashboards.component.text import CTAData, Progress, StatData, Timeline


pytest_plugins = [
    "tests.dashboards.fixtures",
]


@pytest.mark.parametrize(
    "component_class", [Text, Chart, Table, Progress, Timeline, Stat]
)
@pytest.mark.parametrize(
    "component_kwargs",
    [
        {"value": "value"},
        {"defer": lambda **kwargs: "value"},
        {"value": "value", "css_classes": ["a", "b"]},
    ],
)
@pytest.mark.parametrize("htmx", [True, False])
def test_component__renders_value(
    component_class, dashboard, component_kwargs, htmx, rf, snapshot
):
    component = component_class(**component_kwargs)
    component.dashboard = dashboard
    component.key = "test"
    context = Context(
        {
            "component": component,
            "request": rf.get("/"),
        }
    )

    snapshot.assert_match(render_component_test(context, htmx=htmx))


@pytest.mark.parametrize("htmx", [True, False])
def test_cta_component__renders_value(htmx, dashboard, rf, snapshot):
    component = CTA(value=CTAData(text="click here", href="/"))
    component.key = "test"
    component.dashboard = dashboard
    context = Context(
        {
            "component": component,
            "request": rf.get("/"),
        }
    )

    snapshot.assert_match(render_component_test(context, htmx=htmx))


@pytest.mark.parametrize(
    "component_kwargs",
    [
        {"value": StatData(text="100%", sub_text="increase")},
        {"defer": lambda **k: StatData(text="100%", sub_text="increase")},
        {
            "value": StatData(
                text="100%", sub_text="increase", change_by=1.0, change_by_text="Change"
            )
        },
    ],
)
@pytest.mark.parametrize("htmx", [True, False])
def test_component__renders_value__stat(
    component_kwargs, dashboard, htmx, rf, snapshot
):
    component = Stat(**component_kwargs)
    component.dashboard = dashboard
    component.key = "test"
    context = Context(
        {
            "component": component,
            "request": rf.get("/"),
        }
    )

    snapshot.assert_match(render_component_test(context, htmx=htmx))
