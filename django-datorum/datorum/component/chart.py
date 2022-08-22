from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from .base import Component


@dataclass
class Chart(Component):
    render_json: bool = True
    template: str = "datorum/components/chart/chart.html"


@dataclass
class ChartData:
    @dataclass
    class Trace:
        class Mode(Enum):
            LINE = "lines"
            SCATTER = "markers"
            SCATTER_LINE = "lines+markers"

        class Type(Enum):
            BAR = "bar"
            SCATTER = "scatter"

        x: list[Any]
        y: list[Any]
        type: Mode
        mode: Type
        name: Optional[str]

    traces: list[Trace]
    layout: Optional[dict[str, str]] = None
