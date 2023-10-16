from dataclasses import dataclass

from .base import Component
from .stat import *


@dataclass
class Text(Component):
    template_name: str = "dashboards/components/text/text.html"
    mark_safe: bool = False
