from django.template import Context
from django.test.utils import override_settings

import pytest

from tests import urls
from tests.utils import render_dashboard_test
from wildcoeus.dashboards.component.layout import (
    HTML,
    Card,
    ComponentLayout,
    Div,
    Tab,
    TabContainer,
)


pytest_plugins = [
    "tests.dashboards.fixtures",
]


@override_settings(ROOT_URLCONF=urls)
def test_dashboard__render_layout(rf, dashboard_with_layout, snapshot):
    context = Context(
        {
            "dashboard": dashboard_with_layout,
            "request": rf.get("/"),
        }
    )

    snapshot.assert_match(render_dashboard_test(context))


@override_settings(ROOT_URLCONF=urls)
@pytest.mark.parametrize("component_class", [Div, Tab, Card])
def test_html_component__render(rf, component_class, dashboard, snapshot):
    request = rf.get("/")
    context = Context({"request": request})

    snapshot.assert_match(
        component_class("component_1", css_classes="css_class").render(
            dashboard=dashboard(request=request), context=context
        )
    )


def test_tab_container__render(rf, dashboard, snapshot):
    request = rf.get("/")
    context = Context({"request": request})

    snapshot.assert_match(
        TabContainer(
            Tab(HTML("some text....")),
        ).render(dashboard=dashboard(request=request), context=context)
    )


def test_html__render(rf, dashboard, snapshot):
    context = Context({"request": rf.get("/")})

    snapshot.assert_match(
        HTML("some text....").render(dashboard=dashboard, context=context)
    )


@override_settings(ROOT_URLCONF=urls)
def test_layout_component__render(rf, dashboard, snapshot):
    request = rf.get("/")
    context = Context({"request": request})

    snapshot.assert_match(
        ComponentLayout(
            "component_1",
            "component_2",
        ).render(dashboard=dashboard(request=request), context=context)
    )


@override_settings(ROOT_URLCONF=urls)
def test_layout_component__unknown_component_ignored(rf, dashboard, snapshot):
    request = rf.get("/")
    context = Context({"request": request})

    snapshot.assert_match(
        ComponentLayout(
            "component_1",
            "component_2",
            "component_3",
        ).render(dashboard=dashboard(request=request), context=context)
    )
