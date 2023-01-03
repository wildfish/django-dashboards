from django.apps import AppConfig


class ReposConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "demo.repos"

    def ready(self):
        from wildcoeus.pipelines.registry import pipeline_registry

        pipeline_registry.autodiscover_pipelines()
