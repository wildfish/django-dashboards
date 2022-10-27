from dataclasses import dataclass
from typing import Optional

from django.contrib.auth.models import User

from datorum.dashboards.component import Chart, Stat
from datorum.dashboards.component.text import StatData
from datorum.dashboards.types import ValueData


@dataclass
class SSEStat(Stat):
    template: str = "datorum/dashboards/components/sse_stat.html"
    poll_rate: Optional[int] = 10

    @staticmethod
    def pushpin_url():
        """
        Assuming docker pushpin is running, in real world this would be proxied to application.
        """
        return "http://localhost:7999/events/"


@dataclass
class SSEChart(Chart):
    template: str = "datorum/dashboards/components/sse_chart.html"
    poll_rate: Optional[int] = None

    @staticmethod
    def pushpin_url():
        """
        Assuming docker pushpin is running, in real world this would be proxied to application.
        """
        return "http://localhost:7999/events/"


@dataclass
class SharedComponent(Stat):
    """
    Example of a component, where value is set at a class level so the component can be added simply as

        SharedComponent()
    """

    value: ValueData = lambda **kwargs: StatData(
        text=User.objects.count(), sub_text="User Count"
    )
