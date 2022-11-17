from django import forms
from django.urls import reverse

from wildcoeus.dashboards.forms import DashboardForm


pytest_plugins = [
    "tests.dashboards.fixtures",
]


class TestForm(DashboardForm):
    name = forms.CharField()
    number = forms.ChoiceField(
        choices=(
            ("one", "one"),
            ("two", "two"),
            ("three", "three"),
        )
    )


def test_dashboard_form__asdict(dashboard, snapshot):
    form = TestForm(
        app_label=dashboard.Meta.app_label,
        dashboard_class=dashboard,
        key="test",
    )

    snapshot.assert_match(form.asdict())


def test_dashboard_form__get_submit_url(dashboard):
    form = TestForm(
        app_label=dashboard.Meta.app_label,
        dashboard_class=dashboard,
        key="test",
    )

    assert form.get_submit_url() == reverse(
        "wildcoeus.dashboards:form_component",
        args=[dashboard.Meta.app_label, dashboard, "test"],
    )
