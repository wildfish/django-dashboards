from dataclasses import dataclass
from typing import Optional

from datorum.component import Chart, Stat


@dataclass
class SSEStat(Stat):
    template: str = "datorum/components/sse_stat.html"
    poll_rate: Optional[int] = 10

    @staticmethod
    def pushpin_url():
        """
        Assuming docker pushpin is running, in real world this would be proxied to application.
        """
        return "http://localhost:7999/events/"


@dataclass
class SSEChart(Chart):
    template: str = "datorum/components/sse_chart.html"
    poll_rate: Optional[int] = None

    @staticmethod
    def pushpin_url():
        """
        Assuming docker pushpin is running, in real world this would be proxied to application.
        """
        return "http://localhost:7999/events/"
