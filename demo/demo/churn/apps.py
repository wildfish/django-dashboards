from django.apps import AppConfig


class ChurnConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "demo.churn"

    def ready(self):
        # for registry
        import demo.churn.dashboards  # type: ignore
