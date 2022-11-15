from dataclasses import dataclass
from typing import Callable, Optional

from django.http import HttpRequest

from .base import Component


@dataclass
class Chart(Component):
    template: str = "wildcoeus/dashboards/components/chart/chart.html"
    displayModeBar: Optional[bool] = True
    staticPlot: Optional[bool] = False

    # Charts return json or for now str, we need better validation around this.
    # we should also probably accept objects which have a to_json() on them
    value: Optional[str] = None
    defer: Optional[Callable[[HttpRequest], str]] = None
