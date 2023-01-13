import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

import configurations  # noqa: E402
configurations.setup()

app = Celery("demo")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(["wildcoeus.pipelines.runners.celery.tasks"])
