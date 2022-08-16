from django.template import Context

from datorum.component import Text
from datorum.tests.utils import render_component_test


def test_text__renders_value(rf, snapshot):
    context = Context(
        {
            "component": Text(
                value="value",
            ),
            "request": rf.get("/"),
        }
    )

    snapshot.assert_match(render_component_test(context, htmx=False))


def test_text__deferred_value_not_shown(rf, snapshot):
    context = Context(
        {
            "component": Text(
                defer=lambda _: "value",
            ),
            "request": rf.get("/"),
        }
    )

    snapshot.assert_match(render_component_test(context, htmx=True))


def test_text__deferred_value_shown(rf, snapshot):
    context = Context(
        {
            "component": Text(
                defer=lambda _: "value",
            ),
            "request": rf.get("/"),
        }
    )

    snapshot.assert_match(render_component_test(context, htmx=False))
