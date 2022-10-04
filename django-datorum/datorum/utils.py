from datetime import datetime
from functools import reduce
from typing import Dict, Any, Optional

from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.utils.functional import cached_property

from datorum.registry import registry

from .exceptions import DashboardNotFoundError


def get_dashboard_class(app_label: str, dashboard_class: str):
    try:
        dashboard = registry.get_by_classname(app_label, dashboard_class)
    except IndexError:
        raise DashboardNotFoundError(
            f"Dashboard {dashboard_class} not found in registry"
        )

    return dashboard.__class__


class BaseFilter:
    def __init__(self, filters, fields):
        self.filters = filters
        self.fields = fields

    def filter(self, qs):
        return qs


class BaseSort:
    def __init__(self, filters, fields):
        self.filters = filters
        self.fields = fields

    def sort(self, qs):
        return qs


class DatatablesQuerysetFilter(BaseFilter):
    def filter(self, qs):
        """
        Apply ordering based on the search[value] and columns[{field}][search][value] column request params.
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
    def sort(self, qs):
        """
        Apply ordering based on the order[{field}][column] column request params.
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
    def sort(self, data):
        """
        Apply ordering based on the order[{field}][column] column request params.
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
    def filter(self, data):
        """
        Apply ordering based on the search[value] and columns[{field}][search][value] column request params.
        """

        global_search_value = self.filters.get("search[value]")

        if global_search_value:
            data = [d for d in data if any([global_search_value.lower() in str(x).lower() for x in d.values()])]

        return data


class ReactTablesQuerysetSort(BaseSort):
    def sort(self, qs):
        """
        Apply ordering based on the order[{field}][column] column request params.
        """
        direction = "asc"

        if "sortby" in self.filters:
            field = F(self.filters["sortby"])

            if "direction" in self.filters:
                direction = self.filters["direction"]

            sort_by = field.desc(nulls_last=True) if direction == "desc" else field.asc(nulls_last=True)

            qs = qs.order_by(sort_by)

        return qs


class ReactTablesSort(BaseSort):
    def sort(self, data):
        """
        Apply ordering based on the order[{field}][column] column request params.
        """
        direction = "asc"
        # todo: can this be generic with react tables?
        if "sortby" in self.filters:
            sort_by = self.filters["sortby"]

            if "direction" in self.filters:
                direction = self.filters["direction"]

            data = sorted(data, key=lambda x: x[sort_by], reverse=direction == "desc")

        return data


class ToTable:
    """
    Transform a QS to datatables response based on request. Only supports filtering/search as required atm:

        - Global search.
        - Field search.
        - Field/Multi field ordering.
    """
    def __init__(self, data: Any, filters: Dict, field_to_name: Dict, count_func, first_as_absolute_url: bool = False, filter_class: Optional[DatatablesQuerysetFilter] = None, sort_class: Optional[DatatablesQuerysetSort] = None):
        self.data = data
        self.filters = filters
        self.field_to_name = field_to_name
        self.first_as_absolute_url = first_as_absolute_url
        self.count_func = count_func
        self.filter_class = filter_class
        self.sort_class = sort_class

    def _paginate(self, start, length):
        paginator = Paginator(self.data, length)
        page_number = (int(start) / int(length)) + 1
        return paginator.get_page(page_number), paginator.count

    @cached_property
    def field_def(self):
        return self.field_to_name

    @cached_property
    def fields(self):
        return list(self.field_def.keys())

    def filter(self, start, length):
        """
        Render paginated, filtered and orders results into a format expected by datatables.
        """
        initial_count = self.count_func(self.data)
        if self.sort_class:
            self.data = self.sort_class(self.filters, self.fields).sort(self.data)

        if self.filter_class:
            self.data = self.filter_class(self.filters, self.fields).filter(self.data)

        page_obj, filtered_count = self._paginate(start, length)

        data = []

        for obj in page_obj.object_list:
            values = {}
            fields = self.fields
            for field in fields:
                # reduce is used to allow relations to be traversed.
                try:
                    value = reduce(getattr, field.split("__"), obj)
                except AttributeError:
                    value = obj.get(field)

                if value and isinstance(value, datetime):
                    value = naturaltime(value)

                elif isinstance(value, bool):
                    value = "Yes" if value else "No"

                elif value is None:
                    value = "-"

                if field == fields[0] and self.first_as_absolute_url:
                    values[field] = f'<a href="{obj.get_absolute_url()}">{value}</a>'
                else:
                    values[field] = value
            data.append(values)

        return {
            "recordsTotal": initial_count,
            "recordsFiltered": filtered_count,
            "data": data,
            "page_count": page_obj.paginator.num_pages,
            "page": page_obj.number,
        }

    def filter_data(self, start, length):
        return self.filter(start, length)
