from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional, Union

from django.http import HttpRequest

from .base import Component


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
        text: Optional[list] = None
        type: Optional[Type] = None
        mode: Optional[Mode] = None
        name: Optional[str] = None
        marker: Optional[dict] = field(default_factory=lambda: {})

    @dataclass
    class Gauge:
        class Mode(Enum):
            STANDARD = "gauge+number"
            DELTA = "gauge+number+delta"

        domain: dict
        value: int
        title: Optional[dict] = None
        mode: Optional[Mode] = None
        delta: Optional[dict] = None
        gauge: Optional[dict] = None
        type: str = "indicator"

    @dataclass
    class Sankey:
        type: str = "sankey"
        orientation: str = "h"
        arrangement: str = "fixed"
        node: Optional[dict] = None
        link: Optional[dict] = None

    data: list[Union[Gauge, Trace, Sankey, Any]]
    layout: Optional[dict[str, str]] = None


@dataclass
class Chart(Component):
    template: str = "datorum/components/chart/chart.html"

    # Expect charts to return chart data
    value: Optional[ChartData] = None
    defer: Optional[Callable[[HttpRequest], ChartData]] = None
