from django import forms

from dashboards.forms import DashboardForm


class ExampleForm(DashboardForm):
    country = forms.ChoiceField(
        choices=(
            ("all", "All"),
            ("na", "North America"),
            ("europe", "Europe"),
            ("asia", "Asia/Pacific"),
        )
    )


class MedalForm(DashboardForm):
    medal = forms.ChoiceField(
        choices=(
            ("all", "All"),
            ("gold", "Gold"),
            ("silver", "Silver"),
            ("bronze", "Bronze"),
        )
    )
