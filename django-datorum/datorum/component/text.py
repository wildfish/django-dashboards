from dataclasses import dataclass

from .base import Component


@dataclass
class Text(Component):
    template: str = "datorum/components/text/text.html"


@dataclass
class HTML(Component):
    template: str = "datorum/components/text/html.html"


@dataclass
class Stat(Component):
    template: str = "datorum/components/text/stat.html"
