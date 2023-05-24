from django.template import Context

import pytest

from dashboards.component import Gauge
from dashboards.component.gauge.gauge import GaugeValue
from tests.utils import render_component_test


pytest_plugins = [
    "tests.dashboards.fixtures",
]


@pytest.mark.parametrize("htmx", [True, False])
def test_gauge_component__renders_value(htmx, dashboard, rf, snapshot):
    component = Gauge(value=GaugeValue(value=50, max=100))
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
        {"value": GaugeValue(value=50, max=100)},
        {"defer": lambda **k: GaugeValue(value=50, max=100)},
        {"value": GaugeValue(value=50, max=100, min=-100)},
        {"value": GaugeValue(value=50, max=100, sub_text="foo")},
        {"value": GaugeValue(value=50, max=100, value_text="bar")},
    ],
)
@pytest.mark.parametrize("htmx", [True, False])
def test_stat_component__renders_value(component_kwargs, dashboard, htmx, rf, snapshot):
    component = Gauge(**component_kwargs)
    component.dashboard = dashboard
    component.key = "test"
    context = Context(
        {
            "component": component,
            "request": rf.get("/"),
        }
    )

    snapshot.assert_match(render_component_test(context, htmx=htmx))
