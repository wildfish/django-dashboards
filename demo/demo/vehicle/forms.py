from django import forms

from datorum.forms import DatorumForm

from .models import Vehicle


class VehicleTypeFilterForm(DatorumForm):
    vehicle_type = forms.ChoiceField(
        choices=[("", "all")] + Vehicle.TruckType.choices,
        required=False,
    )
