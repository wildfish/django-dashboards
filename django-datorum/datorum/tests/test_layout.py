from django.template import Context
from django.test.utils import override_settings

import pytest

from datorum.views import DashboardView

from ..component.layout import HTML, Card, ComponentLayout, Div, Tab, TabContainer
from . import urls


pytest_plugins = [
    "datorum.tests.fixtures",
]


@override_settings(ROOT_URLCONF=urls)
def test_dashboard__render_layout(rf, dashboard_with_layout, snapshot):
    request = rf.get("/")
    request.htmx = False
    view = DashboardView(dashboard_class=dashboard_with_layout)
    view.setup(request)

    snapshot.assert_match(view.get(request).rendered_content)


@override_settings(ROOT_URLCONF=urls)
@pytest.mark.parametrize("component_class", [Div, Tab, Card])
def test_html_component__render(rf, component_class, dashboard, snapshot):
    context = Context({"request": rf.get("/")})

    snapshot.assert_match(
        component_class("component_1", css_classes="css_class").render(
            dashboard=dashboard, context=context
        )
    )


def test_tab_container__render(rf, dashboard, snapshot):
    context = Context({"request": rf.get("/")})

    snapshot.assert_match(
        TabContainer(
            Tab(HTML("some text....")),
        ).render(dashboard=dashboard, context=context)
    )


def test_html__render(rf, dashboard, snapshot):
    context = Context({"request": rf.get("/")})

    snapshot.assert_match(
        HTML("some text....").render(dashboard=dashboard, context=context)
    )


@override_settings(ROOT_URLCONF=urls)
def test_layout_component__render(rf, dashboard, snapshot):
    context = Context({"request": rf.get("/")})

    snapshot.assert_match(
        ComponentLayout(
            "component_1",
            "component_2",
        ).render(dashboard=dashboard, context=context)
    )


@override_settings(ROOT_URLCONF=urls)
def test_layout_component__unknown_component_ignored(rf, dashboard, snapshot):
    context = Context({"request": rf.get("/")})

    snapshot.assert_match(
        ComponentLayout(
            "component_1",
            "component_2",
            "component_3",
        ).render(dashboard=dashboard, context=context)
    )
