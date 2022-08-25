from dataclasses import dataclass
from typing import Callable, Optional, Union

from django.http import HttpRequest

from .base import Component


@dataclass
class MapData:
    @dataclass
    class ScatterGeo:
        lon: float
        lat: float
        line: Optional[dict]
        locationmode = Optional[str]
        type: str = "scattergeo"
        mode: str = "lines"

    @dataclass
    class Choropleth:
        locations: list
        z: list
        text: list
        locationmode: Optional[str]
        type: str = "choropleth"
        autocolorscale: bool = True

    @dataclass
    class MapLayout:
        title: str
        geo: Optional[dict]
        showlegend: bool = False

    data: list[Union[ScatterGeo, Choropleth]]
    layout: Optional[dict[str, str]] = None


@dataclass
class Map(Component):
    render_json: bool = True
    template: str = "datorum/components/map/map.html"

    # Expect map to return map data
    value: Optional[MapData] = None
    defer: Optional[Callable[[HttpRequest], MapData]] = None
