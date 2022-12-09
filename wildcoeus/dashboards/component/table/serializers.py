from datetime import datetime
from functools import reduce
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.paginator import Page, Paginator
from django.db.models import QuerySet

from wildcoeus.dashboards.log import logger

from .mixins import TableMixin
from .table import TableData


class TableSerializer(TableMixin):
    """
    Applies filtering, sorting and pagination to a dataset before returning.  Based on datatables
    """

    def __init__(
        self,
        filters: Dict[str, Any],
        fields: List[str],
        first_as_absolute_url: bool = False,
        force_lower: bool = True,
        field_modifiers: Optional[Dict[str, Callable]] = None,
    ):
        self.filters = filters
        self.fields = fields
        self.first_as_absolute_url = first_as_absolute_url
        self.force_lower = force_lower
        self.field_modifiers = field_modifiers

    def apply_paginator(
        self, data: Union[QuerySet, List], start: int, length: int
    ) -> Tuple[Page, int]:
        paginator = Paginator(data, length)
        page_number = (int(start) / int(length)) + 1
        return paginator.get_page(page_number), paginator.count

    def _process_data(self, data: Union[QuerySet, List], start: int, length: int):
        # apply filtering
        data = self.filter(data)

        # apply sorting
        data = self.sort(data)

        # apply pagination
        page_obj, filtered_count = self.apply_paginator(data, start, length)

        processed_data = []

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

                if self.field_modifiers and field in self.field_modifiers.keys():
                    value = self.field_modifiers[field](obj)

                values[field] = value

            processed_data.append(values)

        return processed_data, filtered_count

    def serialize(
        self,
        data: Union[QuerySet, List],
        start: int,
        length: int,
    ) -> TableData:
        """
        return paginated, filtered and ordered data in a format expected by table.
        """
        # how many results do we have before filtering and paginating
        initial_count = self.count(data)
        # if length is -1 then this means no pagination e.g. show all
        if length < 0:
            length = initial_count

        # apply filtering, sorting and pagination
        processed_data, filtered_count = self._process_data(data, start, length)

        return TableData(
            data=processed_data,
            draw=self.filters.get("draw", 1),
            total=initial_count,
            filtered=filtered_count,
        )
