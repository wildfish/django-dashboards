from dataclasses import dataclass
from typing import Callable, Optional, Type, Union

from dashboards import config
from dashboards.component import Component
from dashboards.component.table import SerializedTable, TableSerializer


@dataclass
class BasicTable(Component):
    """
    Basic HTML Table without any js.
    """

    template_name: str = "dashboards/components/table/basic.html"
    value: Optional[Union[Callable[..., SerializedTable], Type[TableSerializer]]] = None
    defer: Optional[Union[Callable[..., SerializedTable], Type[TableSerializer]]] = None

    def __post_init__(self):
        default_css_classes = config.Config().DASHBOARDS_COMPONENT_CLASSES["Table"]
        # make sure css_classes is a dict as this is what form template requires
        if self.css_classes and isinstance(self.css_classes, str):
            # if sting assume this is form class
            self.css_classes = {"table": self.css_classes}

        # update defaults with any css classes which have been passed in
        if isinstance(default_css_classes, dict) and isinstance(self.css_classes, dict):
            default_css_classes.update(self.css_classes)

        self.css_classes = default_css_classes


@dataclass
class DataTable(BasicTable):
    """
    HTML Table with js for pagination, sorting, filtering etc.
    """

    template_name: str = "dashboards/components/table/index.html"
    page_size: int = 10
    searching: Optional[bool] = True
    paging: Optional[bool] = True
    ordering: Optional[bool] = True

    class Media:
        js = ("dashboards/vendor/js/datatables.min.js",)
        css = {
            "all": ("dashboards/vendor/css/datatables.min.css",),
        }


class Table(DataTable):
    """
    The default table is a DataTable but this could change
    """
