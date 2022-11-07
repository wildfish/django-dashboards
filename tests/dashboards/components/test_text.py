import datetime

from django.template import Context

import pytest

from tests.utils import render_component_test
from wildcoeus.dashboards.component import CTA
from wildcoeus.dashboards.component.text import (
    CTAData,
    Progress,
    ProgressData,
    Stat,
    StatData,
    TimelineData,
)


pytest_plugins = [
    "tests.dashboards.fixtures",
]


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


@pytest.mark.parametrize(
    "component_kwargs",
    [
        {
            "value": ProgressData(
                data=[
                    ProgressData.ProgressItem(value="100%", percentage=100, title=None)
                ]
            )
        },
        {
            "defer": lambda **k: ProgressData(
                data=[
                    ProgressData.ProgressItem(value="100%", percentage=100, title=None)
                ]
            )
        },
        {
            "value": ProgressData(
                data=[
                    ProgressData.ProgressItem(value="100%", percentage=100, title="a"),
                    ProgressData.ProgressItem(value="100%", percentage=100, title="b"),
                ]
            )
        },
    ],
)
@pytest.mark.parametrize("htmx", [True, False])
def test_progress_component__renders_value(
    component_kwargs, dashboard, htmx, rf, snapshot
):
    component = Progress(**component_kwargs)
    component.dashboard = dashboard
    component.key = "test"
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
        {
            "value": TimelineData(
                items=[
                    TimelineData.TimelineItem(
                        icon="<>",
                        title="t1",
                        subtext="st1",
                        datetime=datetime.datetime(2020, 1, 1),
                    )
                ]
            ),
        },
        {
            "defer": lambda **k: TimelineData(
                items=[
                    TimelineData.TimelineItem(
                        icon="<>",
                        title="t1",
                        subtext="st1",
                        datetime=datetime.datetime(2020, 1, 1),
                    )
                ]
            )
        },
        {
            "value": TimelineData(
                items=[
                    TimelineData.TimelineItem(
                        icon="<>",
                        title="t1",
                        subtext="st1",
                        datetime=datetime.datetime(2020, 1, 1),
                    ),
                    TimelineData.TimelineItem(
                        icon="<>",
                        title="t2",
                        subtext="st2",
                        datetime=datetime.datetime(2020, 1, 1),
                    ),
                ]
            ),
        },
    ],
)
@pytest.mark.parametrize("htmx", [True, False])
def test_timeline_component__renders_value(
    component_kwargs, dashboard, htmx, rf, snapshot
):
    component = Progress(**component_kwargs)
    component.dashboard = dashboard
    component.key = "test"
    context = Context(
        {
            "component": component,
            "request": rf.get("/"),
        }
    )

    snapshot.assert_match(render_component_test(context, htmx=htmx))
