import datetime
from dataclasses import dataclass, field
from typing import Callable, Optional

from django.http import HttpRequest

from .base import Component


@dataclass
class Text(Component):
    template_name: str = "wildcoeus/dashboards/components/text/text.html"
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
    template_name: str = "wildcoeus/dashboards/components/text/stat.html"
    href: Optional[str] = None


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
    template_name: str = "wildcoeus/dashboards/components/text/progress.html"
    value: Optional[ProgressData] = None
    defer: Optional[Callable[[HttpRequest], ProgressData]] = None


@dataclass
class TimelineData:
    @dataclass
    class TimelineItem:
        icon: str  # html element
        title: str
        subtext: str
        datetime: datetime.datetime
        css_classes: Optional[str] = "timeline-item"

    items: list[TimelineItem]


@dataclass
class Timeline(Component):
    template_name: str = "wildcoeus/dashboards/components/text/timeline.html"
    value: Optional[TimelineData] = None
    defer: Optional[Callable[[HttpRequest], TimelineData]] = None
