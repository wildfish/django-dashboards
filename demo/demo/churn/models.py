from django.db import models

from django_extensions.db.models import TimeStampedModel


class Customer(TimeStampedModel):
    reference = models.CharField(max_length=20)
    phone = models.CharField(max_length=50)
    email = models.EmailField()


class CustomerRevenue(TimeStampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    year = models.SmallIntegerField()
    revenue = models.FloatField()
