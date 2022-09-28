from django import forms

from datorum.forms import DatorumForm

from .models import Vehicle


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


class VehicleTypeFilterForm(DatorumForm):
    vehicle_type = forms.ChoiceField(
        choices=[("", "all")] + Vehicle.TruckType.choices,
        required=False,
    )
