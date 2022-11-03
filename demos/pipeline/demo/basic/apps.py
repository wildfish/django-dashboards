from django.apps import AppConfig


class BasicConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "demo.basic"

    def ready(self):
        from wildcoeus.pipelines.registry import pipeline_registry

        pipeline_registry.autodiscover_pipelines()
