import collections
from dataclasses import dataclass
from typing import Any, Callable, Optional

from django.http import HttpRequest

from .base import Component


@dataclass
class TableData:
    headers: list[str]
    rows: list[dict[str, Any]]
    last_page: int = 1

    @classmethod
    def get_request_data(cls, request, fields):
        """
        Helper for tabulator, need to think how this functions with Table Data.
        """
        page = request.GET.get("page", 1)
        size = request.GET.get("size", 10)
        sorts = {}
        for r in range(len(fields)):
            sort_field = request.GET.get(f"sort[{r}][field]")
            sort_order = request.GET.get(f"sort[{r}][dir]")
            if sort_field and sort_order:
                sorts[r] = f"{'-' if sort_order == 'desc' else ''}{sort_field}"
        order = collections.OrderedDict(sorted(sorts.items()))

        return page, size, order


@dataclass
class Table(Component):
    """
    Basic table example, we'd also want it to handle pagination/searching/filter/ordering remotely etc.

    That should all be possible via the defer calls, I've set the table to ajax if deferred and that passes
    the params needed to sort/filter etc, we'd just need to handle that in there, we could probably write some helper
    functions maybe here like Tabulator.apply_sort(data) that we could leverage when deferring data.

    Also need a meta/options call, either part of data or part of the component (Component.Options maybe) which can
    be passed to front end for config options and setting titles of columns/widths etc.

    Atm the deferred version of this is a little confusing, if deferred, we load the component in via HTMX because
    that's what is deferred does, but then we don't render the data as ajax is called to get the data s JSON to
    leverage tabulator (and most js table libs) ajax rendering. Might be a better way to do this maybe we need a is_ajax
    also but that feels complicated, this way works for a poc.

    Also need it to be possible to click on columns for list views.
    """

    template: str = "datorum/components/table/index.html"
    page_size: int = 10

    # Expect tables to return table data
    value: Optional[TableData] = None
    defer: Optional[Callable[[HttpRequest], TableData]] = None
