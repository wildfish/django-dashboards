from dataclasses import dataclass
from typing import Optional

from dashboards.component import Component


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

    class Media:
        js = ("dashboards/vendor/js/gauge.min.js",)
