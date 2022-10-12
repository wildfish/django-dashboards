import os
import configurations  # noqa: E402
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

configurations.setup()

app = Celery("demo")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
