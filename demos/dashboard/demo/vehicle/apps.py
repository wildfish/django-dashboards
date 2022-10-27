from django.apps import AppConfig


class VehicleConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "demo.vehicle"

    def ready(self):
        # for registry
        import demo.vehicle.dashboards  # type: ignore # noqa
