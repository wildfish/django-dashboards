from dataclasses import dataclass, field
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
    change_by_text: Optional[str] = None
    sub_text: Optional[str] = ""
    change_by_display: str = field(init=False)

    def __post_init__(self):
        self.change_by_display = (
            self.change_by_text if self.change_by_text else self.change_by
        )


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
