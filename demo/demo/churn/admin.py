from django.contrib import admin

from .models import Customer, Scenario


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "name",
        "location",
        "recurring_revenue",
        "non_recurring_revenue",
        "contract_start_date",
        "contract_end_date",
    )
    list_filter = ("location",)
    search_fields = ("reference", "name")


@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ("name",)
