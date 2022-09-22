from dataclasses import dataclass
from typing import Optional

from .base import Component


@dataclass
class Text(Component):
    template: str = "datorum/components/text/text.html"
    mark_safe: bool = False


@dataclass
class StatData:
    text: str
    sub_text: Optional[str] = ""


@dataclass
class Stat(Component):
    template: str = "datorum/components/text/stat.html"
    href: Optional[str] = None
