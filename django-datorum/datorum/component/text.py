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
    change_by: Optional[float] = None
    sub_text: Optional[str] = ""


@dataclass
class Stat(Component):
    template: str = "datorum/components/text/stat.html"
    href: Optional[str] = None


@dataclass
class CTAData:
    text: str
    href: str


@dataclass
class CTA(Component):
    template: str = "datorum/components/cta.html"
    value: Optional[CTAData] = None


@dataclass
class ProgressData:
    @dataclass
    class ProgressItem:
        value: str
        percentage: int
        title: Optional[str] = None

    data: list[ProgressItem]


@dataclass
class Progress(Component):
    template: str = "datorum/components/text/progress.html"
