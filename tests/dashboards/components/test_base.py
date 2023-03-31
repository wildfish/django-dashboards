from dataclasses import dataclass

from django.template import Context

import pytest

from dashboards.component import Chart, Component, Text
from dashboards.component.text import Stat
from tests.utils import render_component_test


pytest_plugins = [
    "tests.dashboards.fixtures",
]


class TestComponent(Component):
    pass


@dataclass
class TestDataClassValue:
    x: str
    y: str


@pytest.mark.parametrize(
    "component_kwargs,expected",
    [
        ({"defer": lambda: "deferred"}, True),
        ({"defer_url": "url"}, True),
        ({}, False),
    ],
)
def test_is_deferred(component_kwargs, expected):
    assert TestComponent(**component_kwargs).is_deferred == expected


@pytest.mark.parametrize(
    "component_kwargs,expected",
    [
        ({"trigger_on": None}, ""),
        ({"trigger_on": "x"}, "x from:body, "),
        ({}, ""),
    ],
)
def test_htmx_poll_rate(component_kwargs, expected):
    assert TestComponent(**component_kwargs).htmx_trigger_on() == expected


@pytest.mark.parametrize(
    "component_kwargs,expected",
    [
        ({"poll_rate": None}, None),
        ({"poll_rate": 1}, "every 1s"),
        ({"poll_rate": 123}, "every 123s"),
        ({}, None),
    ],
)
def test_htmx_trigger_on(component_kwargs, expected):
    assert TestComponent(**component_kwargs).htmx_poll_rate() == expected


@pytest.mark.parametrize(
    "component_kwargs,call_deferred,expected",
    [
        ({"defer": lambda **k: "deferred"}, True, "deferred"),
        ({"defer": lambda **k: "deferred"}, False, None),
        ({"value": "value"}, False, "value"),
        ({"value": lambda **k: "called value"}, False, "called value"),
        (
            {"value": lambda **k: TestDataClassValue(x="x", y="y")},
            True,
            {"x": "x", "y": "y"},
        ),
    ],
)
def test_get_value(component_kwargs, call_deferred, expected, rf):
    assert (
        TestComponent(**component_kwargs).get_value(
            request=rf.get("/"), call_deferred=call_deferred, filters={}
        )
        == expected
    )


@pytest.mark.parametrize(
    "component_kwargs,expected",
    [
        ({}, "/dash/app1/testdashboard/@component/None/"),
        (
            {"defer_url": lambda **k: k},
            {
                "reverse_args": [
                    "app1",
                    "testdashboard",
                    None,
                ]
            },
        ),
    ],
)
def test_get_absolute_url(component_kwargs, expected, dashboard):
    component = TestComponent(**component_kwargs)
    component.dashboard = dashboard

    assert component.get_absolute_url() == expected


@pytest.mark.django_db
@pytest.mark.parametrize(
    "component_kwargs,expected",
    [
        ({}, "/dash/app1/testdashboard/1/@component/first/"),
        (
            {"defer_url": lambda **k: k},
            {
                "reverse_args": [
                    "app1",
                    "testdashboard",
                    1,
                    "first",
                ]
            },
        ),
    ],
)
def test_get_absolute_url__with_object(component_kwargs, expected, dashboard, user):
    component = TestComponent(**component_kwargs)
    component.dashboard = dashboard
    component.object = user
    component.key = "first"

    assert component.get_absolute_url() == expected


@pytest.mark.parametrize("component_class", [Text, Chart, Stat])
@pytest.mark.parametrize(
    "component_kwargs",
    [
        {"value": "value"},
        {"defer": lambda **kwargs: "value"},
        {"value": "value", "css_classes": ["a", "b"]},
    ],
)
@pytest.mark.parametrize("htmx", [True, False])
def test_render(component_class, dashboard, component_kwargs, htmx, rf, snapshot):
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
