from dataclasses import dataclass
from datetime import datetime
from functools import reduce
from typing import Any, Dict, List, Optional, Tuple, Union

from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.exceptions import ImproperlyConfigured
from django.core.paginator import Page, Paginator
from django.db.models import QuerySet

from wildcoeus.dashboards.log import logger

from .mixins import TableMixin


@dataclass
class SerializedTable:
    data: List[Dict[str, Any]]
    columns: Dict[str, Any]
    columns_datatables: List[Dict[str, Any]]
    draw: Optional[int] = 0
    total: Optional[int] = 0
    filtered: Optional[int] = 0


class TableSerializerType(type):
    def __new__(mcs, name, bases, attrs):
        table_serializer_class = super().__new__(mcs, name, bases, attrs)
        attr_meta = attrs.get("Meta", None)
        meta = attr_meta or getattr(table_serializer_class, "Meta", None)
        base_meta = getattr(table_serializer_class, "_meta", None)
        table_serializer_class._meta = meta

        if base_meta:
            if not hasattr(meta, "columns"):
                if not hasattr(base_meta, "columns"):
                    raise ImproperlyConfigured("Table must have columns defined")
                table_serializer_class._meta.columns = base_meta.columns
            if not hasattr(meta, "title"):
                table_serializer_class._meta.title = base_meta.title
            if not hasattr(meta, "model"):
                table_serializer_class._meta.model = base_meta.model
            if not hasattr(meta, "first_as_absolute_url"):
                table_serializer_class._meta.first_as_absolute_url = (
                    base_meta.first_as_absolute_url
                )
            if not hasattr(meta, "force_lower"):
                table_serializer_class._meta.force_lower = base_meta.force_lower

        return table_serializer_class


class TableSerializer(TableMixin, metaclass=TableSerializerType):
    """
    Applies filtering, sorting and pagination to a dataset before returning.

    SerializedTable returns the in a format accepted by datatables.js
    """

    class Meta:
        columns: Dict[str, str]
        title: Optional[str] = None
        model: Optional[str] = None
        first_as_absolute_url = False
        force_lower = True

    @classmethod
    def serialize(cls, **serialize_kwargs) -> SerializedTable:
        self = cls()
        filters = serialize_kwargs.get("filters")
        data = self.get_data(**serialize_kwargs)

        start = 0
        length = 5
        draw = 1
        if filters:
            start = int(filters.get("start", start))
            length = int(filters.get("length", length))
            draw = int(filters.get("draw", draw))
        else:
            filters = {}

        # how many results do we have before filtering and paginating
        initial_count = self.count(data)
        # if length is -1 then this means no pagination e.g. show all
        if length < 0:
            length = initial_count

        # apply filtering, sorting and pagination
        data = self.filter(data, filters)
        data = self.sort(data, filters)
        page_obj, filtered_count = self.apply_paginator(data, start, length)

        processed_data = []

        for obj in page_obj.object_list:
            values = {}
            fields = list(self.Meta.columns.keys())
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
                    and self.Meta.first_as_absolute_url
                    and hasattr(obj, "get_absolute_url")
                ):
                    value = f'<a href="{obj.get_absolute_url()}">{value}</a>'

                if hasattr(self, f"get_{field}_value"):
                    value = getattr(self, f"get_{field}_value")(obj)

                values[field] = value

            processed_data.append(values)

        return SerializedTable(
            data=processed_data,
            columns=self.Meta.columns,
            columns_datatables=[
                {"data": d, "title": t} for d, t in self.Meta.columns.items()
            ],
            draw=draw,
            total=initial_count,
            filtered=filtered_count,
        )

    @staticmethod
    def apply_paginator(
        data: Union[QuerySet, List], start: int, length: int
    ) -> Tuple[Page, int]:
        paginator = Paginator(data, length)
        page_number = (int(start) / int(length)) + 1
        return paginator.get_page(page_number), paginator.count

    def get_data(self, *args, **kwargs):
        return self.get_queryset(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        if self._meta.model is not None:
            queryset = self.Meta.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(self)s is missing a QuerySet. Define "
                "%(self)s.model or override "
                "%(self)s.get_queryset()." % {"self": self.__class__.__name__}
            )

        return queryset
