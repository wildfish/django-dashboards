from dataclasses import dataclass
from typing import Any, Callable, Optional

from django.http import HttpRequest

from wildcoeus.dashboards.component import Component


@dataclass
class TableData:
    data: list[dict[str, Any]]
    draw: Optional[int] = 0
    total: Optional[int] = 0
    filtered: Optional[int] = 0


@dataclass
class BasicTable(Component):
    """
    Basic HTML Table without any js.
    """

    template: str = "wildcoeus/dashboards/components/table/basic.html"
    columns: Optional[list] = None
    value: Optional[TableData] = None
    defer: Optional[Callable[[HttpRequest], TableData]] = None
    css_classes: Optional[str] = "table"


@dataclass
class Table(Component):
    """
    HTML Table with js for pagination, sorting, filtering etc.
    """

    template: str = "wildcoeus/dashboards/components/table/index.html"
    page_size: int = 10
    columns: Optional[list] = None
    searching: Optional[bool] = True
    paging: Optional[bool] = True
    ordering: Optional[bool] = True
    value: Optional[TableData] = None
    defer: Optional[Callable[[HttpRequest], TableData]] = None
    poll_rate: Optional[int] = None
