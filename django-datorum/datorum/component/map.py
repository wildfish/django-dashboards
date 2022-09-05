from dataclasses import dataclass
from typing import Callable, Optional, Union, Any

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
        autocolorscale: bool = True
        type: str = "choropleth"

    @dataclass
    class ScatterMapbox:
        lon: float
        lat: float
        marker: Optional[dict]
        type: str = "scattermapbox"
        mode: str = "markers"
        hoverinfo: str = 'text'
        showlegend: bool = True
        customdata: Any = None
        text: list = None
        name: str = None

    @dataclass
    class ChoroplethMapbox:
        geojson: dict
        locations: list
        z: list
        text: list
        featureidkey: str = None
        hoverinfo: str = None
        hoverlabel: dict = None
        marker: dict = None
        colorscale: list = None
        zmin: str = None
        zmax: str = None
        type: str = 'choroplethmapbox'

    data: list[Union[ScatterGeo, Choropleth, ChoroplethMapbox]]
    layout: Optional[dict[str, str]] = None


@dataclass
class Map(Component):
    template: str = "datorum/components/map/map.html"

    # Expect map to return map data
    value: Optional[MapData] = None
    defer: Optional[Callable[[HttpRequest], MapData]] = None
