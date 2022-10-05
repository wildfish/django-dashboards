import collections
from dataclasses import dataclass
from datetime import datetime
from functools import reduce
from typing import Any, Callable, Dict, List, Optional, Type, Union

from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.paginator import Paginator
from django.db.models import F, Q, QuerySet
from django.http import HttpRequest
from django.utils.functional import cached_property

from .base import Component


@dataclass
class TablePaging:
    ssr: bool = False
    page: int = 0
    limit: int = 999
    page_count: int = 1
    sortby: Optional[list[dict[str, Any]]] = None


@dataclass
class TableData:
    data: list[dict[str, Any]]
    # todo: these are for datatables in the mpa only.  need to update FE so can be shared
    draw: int = 0  # datatables only
    recordsTotal: int = 0  # datatables only
    recordsFiltered: int = 0  # datatables only
    page_count: int = 0
    page: int = 0
    # todo: these are for reacttable and spa only.
    paging: Optional[TablePaging] = None

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
    columns: Optional[list] = None

    # Expect tables to return table data
    value: Optional[TableData] = None
    defer: Optional[Callable[[HttpRequest], TableData]] = None


class BaseFilter:
    def __init__(self, filters: Dict[str, Any], fields: List):
        self.filters = filters
        self.fields = fields


class BaseSort:
    def __init__(self, filters: Dict[str, Any], fields: List):
        self.filters = filters
        self.fields = fields


class DatatablesQuerysetFilter(BaseFilter):
    def filter(self, qs: QuerySet):
        """
        Apply filtering on  a queryset based on the search[value] and
        columns[{field}][search][value] column request params.
        """

        global_search_value = self.filters.get("search[value]")

        q_list = Q()

        # Search all fields by adding a Q for each.
        for field in self.fields:
            if global_search_value:
                q_list |= Q(**{f"{field}__icontains": global_search_value})

        # # Search in individual fields by checking for a request value at index.
        for o in range(len(self.fields)):
            field_search_value = self.filters.get(f"columns[{o}][search][value]")
            if field_search_value:
                q_list &= Q(**{f"{self.fields[o]}__icontains": field_search_value})

        return qs.filter(q_list)


class DatatablesQuerysetSort(BaseSort):
    def sort(self, qs: QuerySet):
        """
        Apply ordering to a queryset based on the order[{field}][column] column request params.
        """
        orders = []
        for o in range(len(self.fields)):
            order_index = self.filters.get(f"order[{o}][column]")
            if order_index:
                field = F(self.fields[int(order_index)])
                ordered_field = (
                    field.desc(nulls_last=True)
                    if self.filters.get(f"order[{o}][dir]") == "desc"
                    else field.asc(nulls_last=True)
                )
                orders.append(ordered_field)

        if orders:
            qs = qs.order_by(*orders)

        return qs


class DatatablesSort(BaseSort):
    def sort(self, data: List):
        """
        Apply ordering to a list based on the order[{field}][column] column request params.
        """
        for o in range(len(self.fields)):
            order_index = self.filters.get(f"order[{o}][column]")
            if order_index:
                field = self.fields[int(order_index)]
                direction = self.filters.get(f"order[{o}][dir]")
                # todo: will this work for multiple?
                data = sorted(data, key=lambda x: x[field], reverse=direction == "desc")

        return data


class DatatablesFilter(BaseFilter):
    def filter(self, data: List):
        """
        Apply filtering to a list based on the search[value] request params.
        """

        global_search_value = self.filters.get("search[value]")

        if global_search_value:
            data = [
                d
                for d in data
                if any(
                    [global_search_value.lower() in str(x).lower() for x in d.values()]
                )
            ]

        return data


class ReactTablesQuerysetSort(BaseSort):
    def sort(self, qs: QuerySet):
        """
        Apply ordering to a queryset based on sortby and direction request params.
        """
        direction = "asc"

        if "sortby" in self.filters:
            field = F(self.filters["sortby"])

            if "direction" in self.filters:
                direction = self.filters["direction"]

            sort_by = (
                field.desc(nulls_last=True)
                if direction == "desc"
                else field.asc(nulls_last=True)
            )

            qs = qs.order_by(sort_by)

        return qs


class ReactTablesSort(BaseSort):
    def sort(self, data: List):
        """
        Apply ordering to a list based on a sortby and direction param.
        """
        direction = "asc"
        # only order if sortby provided
        if "sortby" in self.filters:
            sort_by = self.filters["sortby"]

            if "direction" in self.filters:
                direction = self.filters["direction"]

            data = sorted(data, key=lambda x: x[sort_by], reverse=direction == "desc")

        return data


class ToTable:
    """
    Applies filtering, sorting and pagination to a dataset which can be used for datatables and reacttables
    """

    def __init__(
        self,
        data: Union[QuerySet, List],
        filters: Dict[str, Any],
        field_to_name: Dict[str, str],
        count_func: Callable,
        first_as_absolute_url: bool = False,
        filter_class: Optional[
            Union[Type[DatatablesQuerysetFilter], Type[DatatablesFilter]]
        ] = None,
        sort_class: Optional[
            Union[
                Type[DatatablesQuerysetSort],
                Type[DatatablesSort],
                Type[ReactTablesQuerysetSort],
                Type[ReactTablesSort],
            ]
        ] = None,
    ):
        self.data = data
        self.filters = filters
        self.field_to_name = field_to_name
        self.first_as_absolute_url = first_as_absolute_url
        self.count_func = count_func
        self.filter_class = filter_class
        self.sort_class = sort_class

    def _paginate(self, start: int, length: int):
        paginator = Paginator(self.data, length)
        page_number = (int(start) / int(length)) + 1
        return paginator.get_page(page_number), paginator.count

    @cached_property
    def field_def(self):
        return self.field_to_name

    @cached_property
    def fields(self):
        return list(self.field_def.keys())

    def get_data(self, start: int, length: int):
        """
        return paginated, filtered and ordered data in a format expected by table.
        """
        # how many results do we have before filtering and paginating
        initial_count = self.count_func(self.data)

        # apply filtering
        if self.filter_class:
            self.data = self.filter_class(self.filters, self.fields).filter(self.data)

        # apply sorting
        if self.sort_class:
            self.data = self.sort_class(self.filters, self.fields).sort(self.data)

        # apply pagination
        page_obj, filtered_count = self._paginate(start, length)

        data = []

        for obj in page_obj.object_list:
            values = {}
            fields = self.fields
            for field in fields:
                try:
                    # reduce is used to allow relations to be traversed.
                    value = reduce(getattr, field.split("__"), obj)
                except AttributeError:
                    value = obj.get(field)

                if value and isinstance(value, datetime):
                    value = naturaltime(value)

                elif isinstance(value, bool):
                    value = "Yes" if value else "No"

                elif value is None:
                    value = "-"

                if (
                    field == fields[0]
                    and self.first_as_absolute_url
                    and hasattr(obj, "get_absolute_url")
                ):
                    value = f'<a href="{obj.get_absolute_url()}">{value}</a>'

                values[field] = value

            data.append(values)

        return {
            "recordsTotal": initial_count,
            "recordsFiltered": filtered_count,
            "data": data,
            "page_count": page_obj.paginator.num_pages,
            "page": page_obj.number,
        }
