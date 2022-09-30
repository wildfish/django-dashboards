from django.contrib import admin

from .models import Customer


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
