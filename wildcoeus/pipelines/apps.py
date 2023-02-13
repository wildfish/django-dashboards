from django.apps import AppConfig


class PipelinesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wildcoeus.pipelines"
    verbose_name = "Django Wildcoeus Pipelines"

    def ready(self):
        from wildcoeus.pipelines.registry import pipeline_registry
        from wildcoeus.pipelines.tasks import task_registry

        pipeline_registry.autodiscover()
        task_registry.autodiscover()
