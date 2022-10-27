from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "datorum.dashboards"
    verbose_name = "Django Datorum Dashboards"

    def ready(self):
        super(DashboardConfig, self).ready()
