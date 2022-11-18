from django.template import Context

import pytest

from tests.utils import render_dashboard_test
from wildcoeus.dashboards.component.layout import (
    HTML,
    Card,
    ComponentLayout,
    Div,
    Header,
    Tab,
    TabContainer,
)


pytest_plugins = [
    "tests.dashboards.fixtures",
]


def test_dashboard__render_layout(rf, dashboard_with_layout, snapshot):
    context = Context(
        {
            "dashboard": dashboard_with_layout,
            "request": rf.get("/"),
        }
    )

    snapshot.assert_match(render_dashboard_test(context))


@pytest.mark.parametrize("component_class", [Div, Tab, Card])
def test_html_component__render(rf, component_class, dashboard, snapshot):
    request = rf.get("/")
    context = Context({"request": request})

    snapshot.assert_match(
        component_class("component_1", css_classes="css_class").render(
            dashboard=dashboard(request=request), context=context
        )
    )


@pytest.mark.parametrize("component_class", [Div, Tab, Card])
def test_html_component__grid_css_classes__render(rf, component_class, dashboard):
    request = rf.get("/")
    context = Context({"request": request})

    html = component_class("component_1", grid_css_classes="grid-12").render(
        dashboard=dashboard(request=request), context=context
    )

    assert "grid-12" in html


@pytest.mark.django_db
@pytest.mark.parametrize("component_class", [Div, Tab, Card])
def test_html_component__grid_css_classes_not_set__default(
    rf, component_class, dashboard, settings
):
    settings.WILDCOEUS_DEFAULT_GRID_CSS = "default-css-class"

    request = rf.get("/")
    context = Context({"request": request})

    html = component_class("component_1").render(
        dashboard=dashboard(request=request), context=context
    )

    assert "default-css-class" in html


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


def test_header__render(rf, dashboard, snapshot):
    context = Context({"request": rf.get("/")})

    snapshot.assert_match(
        Header(heading="some text....", size=2).render(
            dashboard=dashboard, context=context
        )
    )


def test_layout_component__render(rf, dashboard, snapshot):
    request = rf.get("/")
    context = Context({"request": request})

    snapshot.assert_match(
        ComponentLayout(
            "component_1",
            "component_2",
        ).render(dashboard=dashboard(request=request), context=context)
    )


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
