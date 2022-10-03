from django.forms import ModelForm

from demo.churn.models import Scenario


class ScenarioForm(ModelForm):
    class Meta:
        model = Scenario
        fields = (
            "name",
            "months_as_customer",
            "product_cloud",
            "product_connectivity",
            "product_licenses",
            "product_managed_services",
            "product_backup",
            "product_hardware",
            "faults",
            "sla_breaches",
            "ownership_changes",
            "non_recurring_revenue",
        )
