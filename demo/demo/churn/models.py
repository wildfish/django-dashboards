from django.db import models
from django.db.models import Avg, Count, DecimalField, ExpressionWrapper, Q, Sum
from django.db.models.functions import ExtractMonth, Round

from django_extensions.db.models import TimeStampedModel


class CustomerQuerySet(models.QuerySet):
    def active(self):
        return self.filter(contract_end_date__isnull=True)

    def churned(self):
        return self.filter(contract_end_date__isnull=False)

    def monthly_gross_margin(self):
        return self.churned().aggregate(mgm=Sum("recurring_revenue"))["mgm"]

    def actual_churn_rate(self):
        return self.aggregate(
            churn=ExpressionWrapper(
                Count("pk", filter=Q(contract_end_date__isnull=True)) * 100,
                output_field=DecimalField(),
            )
            / Count("pk")
        )["churn"]

    def average_values(self):
        return self.churned().aggregate(
            average_months_as_customer=Round(Avg(ExtractMonth("contract_start_date"))),
            average_faults=Round(Avg("faults")),
            average_sla_breaches=Round(Avg("sla_breaches")),
            average_ownership_changes=Round(Avg("ownership_changes")),
            average_non_recurring_revenue=Round(Avg("non_recurring_revenue")),
        )


class Customer(TimeStampedModel):
    reference = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    location = models.CharField(max_length=50)

    contract_start_date = models.DateTimeField()
    contract_end_date = models.DateTimeField(null=True)

    product_cloud = models.BooleanField(default=False)
    product_connectivity = models.BooleanField(default=False)
    product_licenses = models.BooleanField(default=False)
    product_managed_services = models.BooleanField(default=False)
    product_backup = models.BooleanField(default=False)
    product_hardware = models.BooleanField(default=False)

    faults = models.IntegerField(default=0)
    sla_breaches = models.IntegerField(default=0)
    ownership_changes = models.IntegerField(default=0)

    recurring_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    non_recurring_revenue = models.DecimalField(max_digits=10, decimal_places=2)

    objects = CustomerQuerySet.as_manager()

    def __str__(self):
        return f"{self.reference}: {self.name}"


class Scenario(TimeStampedModel):
    name = models.CharField(max_length=255)

    months_as_customer = models.IntegerField()

    product_cloud = models.BooleanField(default=False)
    product_connectivity = models.BooleanField(default=False)
    product_licenses = models.BooleanField(default=False)
    product_managed_services = models.BooleanField(default=False)
    product_backup = models.BooleanField(default=False)
    product_hardware = models.BooleanField(default=False)

    faults = models.IntegerField(default=0)
    sla_breaches = models.IntegerField(default=0)
    ownership_changes = models.IntegerField(default=0)
    non_recurring_revenue = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
