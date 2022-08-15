from django import forms

from datorum.forms import DatorumFilterForm


class ExampleForm(DatorumFilterForm):
    country = forms.ChoiceField(
        choices=(
            ("all", "All"),
            ("na", "North America"),
            ("europe", "Europe"),
            ("asia", "Asia/Pacific"),
        )
    )
