from dataclasses import dataclass

from .base import Component


@dataclass
class Text(Component):
    template: str = "datorum/components/text/text.html"
    mark_safe: bool = False


@dataclass
class Stat(Component):
    template: str = "datorum/components/text/stat.html"
