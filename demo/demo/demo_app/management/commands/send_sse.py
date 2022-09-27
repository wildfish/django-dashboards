import time
from random import randint

from django.core.management.base import BaseCommand
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import strip_spaces_between_tags

from datorum.component import Stat
from django_eventstream import send_event


class Command(BaseCommand):
    def handle(self, *args, **options):
        while True:
            value = randint(1, 100)
            rendered = render_to_string(
                Stat.template,
                {
                    "component": Stat(),
                    "rendered_value": {"text": f"{value}%", "sub_text": "Via SSE"},
                },
            )
            parsed = strip_spaces_between_tags(rendered.strip())
            # Here we return a actual rendered stat component, but this could be simply a value JSON also
            send_event("test", "message", parsed, json_encode=False)
            time.sleep(0.5)
