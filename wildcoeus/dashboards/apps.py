from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wildcoeus.dashboards"
    verbose_name = "Django Wildcoeus Dashboards"

    def ready(self):
        super(DashboardConfig, self).ready()
