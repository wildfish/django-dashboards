from dataclasses import dataclass
from typing import Optional

from django.contrib.auth.models import User

from dashboards.component import Chart, Component, Stat
from dashboards.component.text import StatData
from dashboards.types import ValueData


@dataclass
class SSEStat(Stat):
    template_name: str = "dashboards/components/sse_stat.html"
    poll_rate: Optional[int] = 10

    @staticmethod
    def pushpin_url():
        """
        Assuming docker pushpin is running, in real world this would be proxied to application.
        """
        return "http://127.0.0.1:7999/events/"


@dataclass
class SSEChart(Chart):
    template_name: str = "dashboards/components/sse_chart.html"
    poll_rate: Optional[int] = None

    @staticmethod
    def pushpin_url():
        """
        Assuming docker pushpin is running, in real world this would be proxied to application.
        """
        return "http://127.0.0.1:7999/events/"


@dataclass
class SharedComponent(Stat):
    """
    Example of a component, where value is set at a class level so the component can be added simply as

        SharedComponent()
    """

    value: ValueData = lambda **kwargs: StatData(
        text=User.objects.count(), sub_text="User Count"
    )


@dataclass
class GaugeData:
    title: str = ""
    value: Optional[ValueData] = None
    max_value: ValueData = 100


@dataclass
class Gauge(Component):
    template_name: str = "demo/includes/gauge.html"

    class Media:
        js = ("js/svg-gauge.js",)
