from django.template import Context

import pytest

from dashboards.component import CTA
from dashboards.component.text import Text
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
