from django import forms

from datorum.forms import DatorumForm


class ExampleForm(DatorumForm):
    country = forms.ChoiceField(
        choices=(
            ("all", "All"),
            ("na", "North America"),
            ("europe", "Europe"),
            ("asia", "Asia/Pacific"),
        )
    )


class AnimalForm(DatorumForm):
    animal = forms.ChoiceField(
        choices=(
            ("all", "All"),
            ("giraffes", "Giraffe"),
            ("orangutans", "Orangutan"),
            ("monkeys", "Monkey"),
        )
    )
