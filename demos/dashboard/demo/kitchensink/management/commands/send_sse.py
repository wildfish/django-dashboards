import time
from random import randint

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils.html import strip_spaces_between_tags

from django_eventstream import send_event

from datorum.dashboards.component import Stat


class Command(BaseCommand):
    def handle(self, *args, **options):
        while True:

            # sse_stat
            value = randint(1, 100)
            sse_stat = Stat(
                value={"text": f"{value}%", "sub_text": "Via SSE"}, key="sse_stat"
            )
            rendered_stat = render_to_string(
                sse_stat.template,
                {
                    "component": sse_stat,
                    "rendered_value": sse_stat.get_value(),
                },
            )
            parsed_stat = strip_spaces_between_tags(rendered_stat.strip())
            # Here we return a actual rendered stat component, but this could be simply a value JSON also
            send_event("test", "sse_stat", parsed_stat, json_encode=False)

            # sse_chart
            send_event("test", "sse_chart", value, json_encode=False)
            time.sleep(0.5)
