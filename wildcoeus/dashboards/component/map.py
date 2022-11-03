from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Union

from django.http import HttpRequest

from .base import Component


@dataclass
class MapData:
    @dataclass
    class ScatterGeo:
        lon: Optional[list[float]]
        lat: Optional[list[float]]
        line: Optional[dict]
        locationmode = Optional[str]
        text: Optional[list] = None
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
        geojson: Optional[str] = None

    @dataclass
    class ScatterMapbox:
        lon: float
        lat: float
        marker: Optional[dict]
        type: str = "scattermapbox"
        mode: str = "markers"
        hoverinfo: str = "text"
        showlegend: bool = True
        customdata: Optional[Any] = None
        text: Optional[list] = None
        name: Optional[str] = None

    @dataclass
    class ChoroplethMapbox:
        geojson: Dict
        locations: list
        z: list
        text: list
        featureidkey: Optional[str] = None
        hoverinfo: Optional[str] = None
        hoverlabel: Optional[Dict] = None
        marker: Optional[Dict] = None
        colorscale: Optional[list] = None
        zmin: Optional[str] = None
        zmax: Optional[str] = None
        type: Optional[str] = "choroplethmapbox"

    data: list[Union[ScatterGeo, Choropleth, ScatterMapbox, ChoroplethMapbox]]
    layout: Optional[Dict[str, str]] = None


@dataclass
class Map(Component):
    template: str = "wildcoeus/dashboards/components/map/map.html"

    # Expect map to return map data
    value: Optional[MapData] = None
    defer: Optional[Callable[[HttpRequest], MapData]] = None
