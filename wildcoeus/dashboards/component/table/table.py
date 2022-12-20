from dataclasses import dataclass
from typing import Callable, Optional

from wildcoeus.dashboards.component import Component
from wildcoeus.dashboards.component.table import SerializedTable


@dataclass
class BasicTable(Component):
    """
    Basic HTML Table without any js.
    """

    template_name: str = "wildcoeus/dashboards/components/table/basic.html"
    value: Optional[Callable[..., SerializedTable]] = None
    defer: Optional[Callable[..., SerializedTable]] = None
    css_classes: Optional[str] = "table"


@dataclass
class Table(Component):
    """
    HTML Table with js for pagination, sorting, filtering etc.
    """

    template_name: str = "wildcoeus/dashboards/components/table/index.html"
    page_size: int = 10
    searching: Optional[bool] = True
    paging: Optional[bool] = True
    ordering: Optional[bool] = True
    value: Optional[Callable[..., SerializedTable]] = None
    defer: Optional[Callable[..., SerializedTable]] = None
    defer_url: Optional[Callable[..., str]] = None
    poll_rate: Optional[int] = None
