from dataclasses import dataclass

from .base import Component


@dataclass
class Plotly(Component):
    template: str = "datorum/components/chart/plotly.html"
