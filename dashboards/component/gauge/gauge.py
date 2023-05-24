from dataclasses import dataclass, field
from typing import Optional

from dashboards.component import Component
from dashboards.types import ValueData


@dataclass
class GaugeValue:
    value: float
    max: float
    min: Optional[float] = None
    sub_text: Optional[str] = ""
    value_text: Optional[str] = ""


@dataclass
class Gauge(Component):
    title: str = ""
    value: Optional[GaugeValue] = None
    template_name: str = "dashboards/components/gauge/gauge.html"
