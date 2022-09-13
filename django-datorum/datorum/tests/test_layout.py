import pytest
from datorum.views import DashboardView
from django.template import Context
from django.test.utils import override_settings

from ..layout import HTML, Card, Div, LayoutComponent, Tab, TabContainer
from . import urls

pytest_plugins = [
    "datorum.tests.fixtures",
]


@override_settings(ROOT_URLCONF=urls)
def test_dashboard__render_layout(rf, test_dashboard_with_layout, snapshot):
    request = rf.get("/")
    request.htmx = False
    view = DashboardView(dashboard_class=test_dashboard_with_layout)
    view.setup(request)

    snapshot.assert_match(view.get(request).rendered_content)


@override_settings(ROOT_URLCONF=urls)
@pytest.mark.parametrize("component_class", [Div, Tab, Card])
def test_html_component__render(rf, component_class, test_dashboard, snapshot):
    context = Context({"request": rf.get("/")})

    snapshot.assert_match(
        component_class(
            "component_1", element_id="e1", css_class_names="css_class"
        ).render(dashboard=test_dashboard, context=context)
    )


def test_tab_container__render(rf, test_dashboard, snapshot):
    context = Context({"request": rf.get("/")})

    snapshot.assert_match(
        TabContainer(
            Tab(HTML("some text...."), element_id="e1"),
            element_id="e2",
        ).render(dashboard=test_dashboard, context=context)
    )


def test_html__render(rf, test_dashboard, snapshot):
    context = Context({"request": rf.get("/")})

    snapshot.assert_match(
        HTML("some text....").render(dashboard=test_dashboard, context=context)
    )


@override_settings(ROOT_URLCONF=urls)
def test_layout_component__render(rf, test_dashboard, snapshot):
    context = Context({"request": rf.get("/")})

    snapshot.assert_match(
        LayoutComponent(
            "component_1",
            "component_2",
        ).render(dashboard=test_dashboard, context=context)
    )


@override_settings(ROOT_URLCONF=urls)
def test_layout_component__unknown_component_ignored(rf, test_dashboard, snapshot):
    context = Context({"request": rf.get("/")})

    snapshot.assert_match(
        LayoutComponent(
            "component_1",
            "component_2",
            "component_3",
        ).render(dashboard=test_dashboard, context=context)
    )
