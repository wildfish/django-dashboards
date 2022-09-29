from django.apps import AppConfig


class KitchenSinkConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "demo.kitchensink"

    def ready(self):
        # for registry
        import demo.kitchensink.dashboards  # type: ignore
