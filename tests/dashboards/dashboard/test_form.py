from django import forms

from dashboards.forms import DashboardForm


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
    form = TestForm()

    snapshot.assert_match(form.asdict())
