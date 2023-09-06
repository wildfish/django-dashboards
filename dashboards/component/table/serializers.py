from dataclasses import dataclass
from datetime import datetime
from functools import reduce
from typing import Any, Dict, List, Optional, Type

from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model, QuerySet

import asset_definitions

from dashboards.log import logger
from dashboards.meta import ClassWithMeta

from .mixins import TableDataProcessorMixin


@dataclass
class SerializedTable:
    data: List[Dict[str, Any]]
    columns: Dict[str, Any]
    columns_datatables: List[Dict[str, Any]]
    order: List[Any]
    draw: Optional[int] = 0
    total: Optional[int] = 0
    filtered: Optional[int] = 0


class BaseTableSerializer(
    ClassWithMeta, asset_definitions.MediaDefiningClass, TableDataProcessorMixin
):
    class Meta:
        columns: Dict[str, str]
        order: List[str]
        title: Optional[str] = None
        first_as_absolute_url = False
        force_lower = True

    @classmethod
    def preprocess_meta(cls, current_class_meta):
        title = getattr(current_class_meta, "title", None)

        if title and not hasattr(current_class_meta, "name"):
            current_class_meta.name = title

        if title and not hasattr(current_class_meta, "verbose_name"):
            current_class_meta.verbose_name = title

        return current_class_meta

    @classmethod
    def postprocess_meta(cls, current_class_meta, resolved_meta_class):
        if not hasattr(resolved_meta_class, "title"):
            resolved_meta_class.title = resolved_meta_class.verbose_name

        return resolved_meta_class

    @classmethod
    def serialize(cls, **serialize_kwargs) -> SerializedTable:
        self = cls()
        filters = serialize_kwargs.get("filters", {})
        data = self.get_data(**serialize_kwargs)
        columns = self._meta.columns
        fields = list(columns)

        # how many results do we have before table filtering and paginating
        initial_count = self.count(data)

        start = 0
        draw = 1
        length = initial_count

        if filters:
            start = int(filters.get("start", start))
            length = int(filters.get("length", length))
            if length < 1:
                length = initial_count
            draw = int(filters.get("draw", draw))

        # apply filtering, sorting and pagination (datatables)
        data = self.filter(data=data, filters=filters)
        data = self.sort(data=data, filters=filters)
        processed_data = []
        filtered_count = 0

        # do we still have data after filtering, if so paginate and format
        if self.count(data) > 0:
            page_obj, filtered_count = self.apply_paginator(data, start, length)

            for obj in page_obj.object_list:
                values = {}
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
                        and self._meta.first_as_absolute_url
                        and hasattr(obj, "get_absolute_url")
                    ):
                        value = f'<a href="{obj.get_absolute_url()}">{value}</a>'

                    if hasattr(self, f"get_{field}_value"):
                        value = getattr(self, f"get_{field}_value")(obj)

                    values[field] = value

                processed_data.append(values)

        order = [0, "asc"]
        if hasattr(self._meta, "order"):
            order = [
                [
                    fields.index(v.replace("-", "")),
                    "desc" if "-" in v else "asc",
                ]
                for v in self._meta.order
            ]

        return SerializedTable(
            data=processed_data,
            columns=columns,
            columns_datatables=[{"data": d, "title": t} for d, t in columns.items()],
            order=order,
            draw=draw,
            total=initial_count,
            filtered=filtered_count,
        )

    def get_data(self, *args, **kwargs):
        raise NotImplementedError


class TableSerializer(BaseTableSerializer):
    """
    Applies filtering, sorting and pagination to a dataset before returning.

    SerializedTable returns the in a format accepted by datatables.js
    """

    _meta: Type[Any]

    class Meta:
        columns: Dict[str, str]
        order: List[str]
        title: Optional[str] = None
        first_as_absolute_url = False
        force_lower = True
        model: Optional[Model] = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not hasattr(cls._meta, "columns"):
            raise ImproperlyConfigured("Table must have columns defined")

    def get_data(self, *args, **kwargs) -> QuerySet:
        return self.get_queryset(*args, **kwargs)

    def get_queryset(self, *args, **kwargs) -> QuerySet:
        if self._meta.model is not None:
            queryset = self._meta.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(self)s is missing a QuerySet. Define "
                "%(self)s.model or override "
                "%(self)s.get_queryset()." % {"self": self.__class__.__name__}
            )

        return queryset
