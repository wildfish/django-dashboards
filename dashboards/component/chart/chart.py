from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, Optional, Type, Union


if TYPE_CHECKING:
    from dashboards.component.chart import ChartSerializer

from dashboards.component import Component


@dataclass
class Chart(Component):
    template_name: str = "dashboards/components/chart/chart.html"

    value: Optional[Union[Callable[..., Any], Type["ChartSerializer"]]] = None
    defer: Optional[Union[Callable[..., Any], Type["ChartSerializer"]]] = None
