from dataclasses import dataclass, field
from typing import Optional, Union

from .base import Component


@dataclass
class Text(Component):
    template_name: str = "dashboards/components/text/text.html"
    mark_safe: bool = False


@dataclass
class StatData:
    text: str
    change_by: Optional[float] = None
    change_by_text: Optional[str] = None
    sub_text: Optional[str] = ""
    change_by_display: Optional[Union[str, float]] = field(init=False)

    def __post_init__(self):
        self.change_by_display = (
            self.change_by_text if self.change_by_text else self.change_by
        )


@dataclass
class Stat(Component):
    template_name: str = "dashboards/components/text/stat.html"
    href: Optional[str] = None
