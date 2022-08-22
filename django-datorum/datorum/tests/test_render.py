from django.template import Context
from django.test.utils import override_settings

import pytest

from datorum.component import HTML, Chart, Stat, Table, Text
from datorum.tests.utils import render_component_test

from . import urls


@override_settings(ROOT_URLCONF=urls)
@pytest.mark.parametrize("component_class", [Text, HTML, Chart, Table])
@pytest.mark.parametrize(
    "component_kwargs", [{"value": "value"}, {"defer": lambda _: "value"}]
)
@pytest.mark.parametrize("htmx", [True, False])
def test_component__renders_value(
    component_class, component_kwargs, htmx, rf, snapshot
):
    component = component_class(**component_kwargs)
    component.key = "test"
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
        {"defer": lambda _: {"text": "100%", "sub_text": "increase"}},
    ],
)
@pytest.mark.parametrize("htmx", [True, False])
def test_component__renders_value__stat(component_kwargs, htmx, rf, snapshot):
    component = Stat(**component_kwargs)
    component.key = "test"
    context = Context(
        {
            "component": component,
            "request": rf.get("/"),
        }
    )

    snapshot.assert_match(render_component_test(context, htmx=htmx))
