from dataclasses import dataclass
from typing import Callable, Optional

from django.http import HttpRequest

from .base import Component


@dataclass
class Map(Component):
    template_name: str = "dashboards/components/map/map.html"
    responsive: Optional[bool] = True

    # Maps return json or for now str, we need better validation around this.
    # we should also probably accept objects which have a to_json() on them
    value: Optional[str] = None
    defer: Optional[Callable[[HttpRequest], str]] = None
