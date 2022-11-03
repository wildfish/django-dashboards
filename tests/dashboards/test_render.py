from django.template import Context
from django.test.utils import override_settings

import pytest

from tests import urls
from tests.utils import render_component_test
from wildcoeus.dashboards.component import CTA, Chart, Stat, Table, Text
from wildcoeus.dashboards.component.text import CTAData


pytest_plugins = [
    "tests.dashboards.fixtures",
]


@override_settings(ROOT_URLCONF=urls)
@pytest.mark.parametrize("component_class", [Text, Chart, Table])
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


@override_settings(ROOT_URLCONF=urls)
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


@override_settings(ROOT_URLCONF=urls)
@pytest.mark.parametrize(
    "component_kwargs",
    [
        {"value": {"text": "100%", "sub_text": "increase"}},
        {"defer": lambda **kwargs: {"text": "100%", "sub_text": "increase"}},
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
