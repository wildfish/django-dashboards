from dataclasses import dataclass

from datorum.component import Stat


@dataclass
class SSEStat(Stat):
    template: str = "datorum/components/sse_stat.html"

    @staticmethod
    def pushpin_url():
        """
        Assuming docker pushpin is running, in real world this would be proxied to application.
        """
        return "http://localhost:7999/events/"
