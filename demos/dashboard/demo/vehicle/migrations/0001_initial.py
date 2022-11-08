# Generated by Django 4.0.7 on 2022-09-29 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Parameter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                (
                    "cast_type",
                    models.CharField(
                        choices=[
                            ("int", "Integer"),
                            ("float", "Float"),
                            ("str", "String"),
                            ("coord", "Coordinate"),
                            ("datetime", "Date/Time"),
                        ],
                        max_length=10,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Vehicle",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ref", models.CharField(max_length=50, unique=True)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("c1", "Class 1 - Light Duty"),
                            ("c2", "Class 2 - Medium Duty"),
                            ("c3", "Class 3 - Heavy Duty"),
                        ],
                        default="c1",
                        max_length=2,
                    ),
                ),
                ("number_plate", models.CharField(max_length=10, unique=True)),
                ("current_mileage", models.IntegerField(default=0)),
                ("last_service", models.DateField(blank=True, null=True)),
                ("next_mot_due", models.DateField(blank=True, null=True)),
                ("purchase_date", models.DateField(blank=True, null=True)),
                ("last_job_date", models.DateField(blank=True, null=True)),
                (
                    "in_use",
                    models.BooleanField(
                        default=False, help_text="Is the vehicle currently on a job"
                    ),
                ),
                (
                    "available",
                    models.BooleanField(
                        default=True,
                        help_text="Is the vehicle available or is it currently out of service",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Data",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.CharField(blank=True, max_length=250)),
                ("timestamp", models.DateTimeField()),
                (
                    "parameter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="vehicle.parameter",
                    ),
                ),
                (
                    "vehicle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="data",
                        to="vehicle.vehicle",
                    ),
                ),
            ],
        ),
    ]