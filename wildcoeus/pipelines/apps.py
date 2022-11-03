from django.apps import AppConfig


class PipelinesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wildcoeus.pipelines"
    verbose_name = "Django Wildcoeus Pipelines"

    def ready(self):
        super(PipelinesConfig, self).ready()
