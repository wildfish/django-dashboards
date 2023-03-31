from django.template import Context

import pytest

from dashboards.component import CTA
from dashboards.component.text import Stat, StatData, Text
from tests.utils import render_component_test


pytest_plugins = [
    "tests.dashboards.fixtures",
]


@pytest.mark.parametrize("htmx", [True, False])
def test_cta_component__renders_value(htmx, dashboard, rf, snapshot):
    component = Text(value="click here", cta=CTA(href="/"))
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
def test_stat_component__renders_value(component_kwargs, dashboard, htmx, rf, snapshot):
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
