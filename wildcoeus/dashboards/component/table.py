from dataclasses import dataclass
from datetime import datetime
from functools import reduce
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.paginator import Page, Paginator
from django.db.models import F, Q, QuerySet
from django.db.models.functions import Lower
from django.http import HttpRequest

from wildcoeus.dashboards.component import Component
from wildcoeus.dashboards.log import logger


@dataclass
class BasicTableData:
    headers: Optional[List[str]] = None
    rows: Optional[List[List[str]]] = None


@dataclass
class BasicTable(Component):
    """
    Basic HTML Table without any js for pagination, sorting, filtering etc.
    """

    template: str = "wildcoeus/dashboards/components/table/basic.html"
    value: Optional[BasicTableData] = None
    defer: Optional[Callable[[HttpRequest], BasicTableData]] = None
    css_classes: Optional[str] = "table"


@dataclass
class TableData:
    data: list[dict[str, Any]]
    draw: int = 0
    total: int = 0
    filtered: int = 0


@dataclass
class Table(Component):
    """
    Basic HTML Table with js for pagination, sorting, filtering etc.
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


class TableFilter:
    def __init__(self, filters: Dict[str, Any], fields: List):
        self.filters = filters
        self.fields = fields

    def filter(self, data: List) -> List:
        """
        Apply filtering to a list based on the search[value] request params and
        columns[{field}][search][value] column request params.
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
        else:
            fields_to_search = {}

            # Search in individual fields by checking for a request value at index.
            for o, field in enumerate(self.fields):
                field_search_value = self.filters.get(f"columns[{o}][search][value]")
                if field_search_value:
                    fields_to_search[field] = field_search_value

            if fields_to_search:
                data = [
                    d
                    for d in data
                    for field, value in fields_to_search.items()
                    if d[field] == value
                ]
        return data


class TableQuerysetFilter(TableFilter):
    def filter(self, qs: QuerySet) -> QuerySet:
        """
        Apply filtering on  a queryset based on the search[value] and
        columns[{field}][search][value] column request params.
        """

        global_search_value = self.filters.get("search[value]")
        # used to filter out non model fields
        model_fields = [f.name for f in qs.model._meta.get_fields()]

        q_list = Q()

        # Search all fields by adding a Q for each.
        for field in self.fields:
            if field in model_fields and global_search_value:
                q_list |= Q(**{f"{field}__icontains": global_search_value})

        # Search in individual fields by checking for a request value at index.
        for o, field in enumerate(self.fields):
            field_search_value = self.filters.get(f"columns[{o}][search][value]")
            if field in model_fields and field_search_value:
                q_list &= Q(**{f"{self.fields[o]}__icontains": field_search_value})

        return qs.filter(q_list)


class TableSort:
    def __init__(self, filters: Dict[str, Any], fields: List, force_lower: bool = True):
        self.filters = filters
        self.fields = fields
        self.force_lower = force_lower

    def sort(self, data: List) -> List:
        """
        Apply ordering to a list based on the order[{field}][column] column request params.
        """

        def conditionally_apply_lower(v):
            if self.force_lower and isinstance(v, str):
                return v.lower()
            return v

        for o in range(len(self.fields)):
            order_index = self.filters.get(f"order[{o}][column]")
            if order_index is not None:
                field = self.fields[int(order_index)]
                direction = self.filters.get(f"order[{o}][dir]")
                data = sorted(
                    data,
                    key=lambda x: conditionally_apply_lower(x[field]),
                    reverse=direction == "desc",
                )

        return data


class TableQuerysetSort(TableSort):
    def sort(self, qs: QuerySet) -> QuerySet:
        """
        Apply ordering to a queryset based on the order[{field}][column] column request params.
        """
        orders = []
        for o in range(len(self.fields)):
            order_index = self.filters.get(f"order[{o}][column]")
            if order_index is not None:
                if self.force_lower:
                    field = Lower(self.fields[int(order_index)])
                else:
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


class TableSerializer:
    """
    Applies filtering, sorting and pagination to a dataset which can be used for datatables and reacttables
    """

    def __init__(
        self,
        data: Union[QuerySet, List],
        filters: Dict[str, Any],
        fields: List[str],
        count_func: Callable,
        first_as_absolute_url: bool = False,
        filter_class: Optional[Type[TableFilter]] = None,
        sort_class: Optional[Type[TableSort]] = None,
    ):
        self.data = data
        self.filters = filters
        self.fields = fields
        self.first_as_absolute_url = first_as_absolute_url
        self.count_func = count_func
        self.filter_class = filter_class
        self.sort_class = sort_class

    def apply_paginator(self, start: int, length: int) -> Tuple[Page, int]:
        paginator = Paginator(self.data, length)
        page_number = (int(start) / int(length)) + 1
        return paginator.get_page(page_number), paginator.count

    def get(self, start: int, length: int) -> TableData:
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

        # if length is -1 then this means no pagination e.g. show all
        if length < 0:
            length = initial_count

        # apply pagination
        page_obj, filtered_count = self.apply_paginator(start, length)

        data = []

        for obj in page_obj.object_list:
            values = {}
            fields = self.fields
            for field in fields:
                if not isinstance(obj, dict):
                    # reduce is used to allow relations to be traversed.
                    try:
                        value = reduce(getattr, field.split("__"), obj)
                    except AttributeError:
                        logger.warn(f"{field} is not a attribute for this object.")
                        value = None
                else:
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

        return TableData(
            data=data,
            draw=self.filters.get("draw", 1),
            total=initial_count,
            filtered=filtered_count,
        )
