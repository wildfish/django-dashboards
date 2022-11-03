from django import forms

from wildcoeus.dashboards.forms import DashboardForm

from .models import Vehicle


class VehicleTypeFilterForm(DashboardForm):
    vehicle_type = forms.ChoiceField(
        choices=[("", "all")] + Vehicle.TruckType.choices,
        required=False,
    )
