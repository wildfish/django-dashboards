from django.apps import AppConfig


class PipelinesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "datorum.pipelines"
    verbose_name = "Django Datorum Pipelines"

    def ready(self):
        super(PipelinesConfig, self).ready()
