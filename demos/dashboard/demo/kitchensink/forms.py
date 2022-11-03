from django import forms

from wildcoeus.dashboards.forms import DashboardForm


class ExampleForm(DashboardForm):
    country = forms.ChoiceField(
        choices=(
            ("all", "All"),
            ("na", "North America"),
            ("europe", "Europe"),
            ("asia", "Asia/Pacific"),
        )
    )


class AnimalForm(DashboardForm):
    animal = forms.ChoiceField(
        choices=(
            ("all", "All"),
            ("giraffes", "Giraffe"),
            ("orangutans", "Orangutan"),
            ("monkeys", "Monkey"),
        )
    )
