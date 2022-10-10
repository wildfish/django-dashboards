from django.apps import AppConfig


class DatorumPipelinesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "datorum_pipelines"
    verbose_name = "Django Datorum Pipelines"

    def ready(self):
        super(DatorumPipelinesConfig, self).ready()
