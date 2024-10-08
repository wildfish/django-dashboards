import datetime
from collections import namedtuple

from django.db import models
from django.db.models import Q, QuerySet
from django.urls import reverse

from dateutil.relativedelta import relativedelta


class VehicleQueryset(QuerySet):
    def for_type(self, vehicle_type: str):
        return self.filter(type=vehicle_type)

    def available(self):
        return self.filter(available=True, in_use=False)

    def requires_service(self):
        service_date = datetime.date.today() - relativedelta(years=1)
        return self.filter(Q(last_service=None) | Q(last_service__lt=service_date))

    def total_vehicle_count(self):
        return self.count()

    def in_use_count(self):
        return self.filter(in_use=True).count()

    def available_count(self):
        return self.available().count()

    def out_of_service_count(self):
        return self.filter(available=False).count()


class Vehicle(models.Model):
    class TruckType(models.TextChoices):
        CLASS_1 = "c1", "Class 1 - Light Duty"
        CLASS_2 = "c2", "Class 2 - Medium Duty"
        CLASS_3 = "c3", "Class 3 - Heavy Duty"

    ref = models.CharField(max_length=50, unique=True)
    type = models.CharField(
        max_length=2, choices=TruckType.choices, default=TruckType.CLASS_1
    )
    number_plate = models.CharField(max_length=10, unique=True)
    current_mileage = models.IntegerField(default=0)
    last_service = models.DateField(null=True, blank=True)
    next_mot_due = models.DateField(null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    last_job_date = models.DateField(null=True, blank=True)
    in_use = models.BooleanField(
        default=False, help_text="Is the vehicle currently on a job"
    )
    available = models.BooleanField(
        default=True,
        help_text="Is the vehicle available or is it currently out of service",
    )

    objects = VehicleQueryset.as_manager()

    def get_locations_for_last_job(self):
        p, _ = Parameter.objects.get_or_create(name="Current Location")
        qs = self.data.select_related("parameter").filter(parameter=p)
        if self.last_job_date:
            qs = qs.filter(timestamp__gte=self.last_job_date)

        qs = qs.order_by("-timestamp")

        return list(map(lambda x: x.convert(), qs))

    def get_absolute_url(self):
        return reverse(
            "dashboards:vehicle_vehicledetaildashboard_detail",
            args=[self.pk],
        )


class Parameter(models.Model):
    class CastType(models.TextChoices):
        INT = "int", "Integer"
        FLOAT = "float", "Float"
        STR = "str", "String"
        COORDINATE = "coord", "Coordinate"
        DATETIME = "datetime", "Date/Time"

    name = models.CharField(max_length=100, unique=True)
    cast_type = models.CharField(max_length=10, choices=CastType.choices)


class Data(models.Model):
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.DO_NOTHING, related_name="data"
    )
    value = models.CharField(max_length=250, blank=True)
    parameter = models.ForeignKey(Parameter, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField()

    DT_FORMAT = "%m-%d-%Y %H:%M:%S"

    def __str__(self):
        return self.value

    def convert(self):
        if self.parameter.cast_type == "str":
            return self.value
        elif self.parameter.cast_type == "int":
            return int(self.value)
        elif self.parameter.cast_type == "float":
            return float(self.value)
        elif self.parameter.cast_type == "coord":
            coord = self.value[1:-1]
            coord = coord.split(",")
            lon = float(coord[0].strip())
            lat = float(coord[1].strip())
            Coord = namedtuple("Coord", ["lon", "lat"])
            return Coord(lon=lon, lat=lat)
        elif self.parameter.cast_type == "datetime":
            return datetime.strptime(self.value, self.DT_FORMAT)  # type: ignore
