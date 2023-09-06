from collections.abc import Iterable
from typing import Any, Dict, List, Tuple, Type, Union

from django.core.exceptions import FieldDoesNotExist
from django.core.paginator import Page, Paginator
from django.db.models import CharField, F, Q, QuerySet
from django.db.models.functions import Lower


class TableQuerysetProcessor:
    @staticmethod
    def filter(qs: QuerySet, fields: List[str], filters: Dict[str, Any]) -> QuerySet:
        """
        Apply filtering on a queryset based on the search[value] and
        columns[{field}][search][value] column request params.
        """

        global_search_value = filters.get("search[value]")
        # used to filter out non model fields
        model_fields = [f.name for f in qs.model._meta.get_fields()]

        q_list = Q()
        # Search all fields by adding a Q for each.
        for field in fields:
            if field in model_fields and global_search_value:
                q_list |= Q(**{f"{field}__icontains": global_search_value})

        # Search in individual fields by checking for a request value at index.
        for o, field in enumerate(fields):
            field_search_value = filters.get(f"columns[{o}][search][value]")
            if field in model_fields and field_search_value:
                q_list &= Q(**{f"{fields[o]}__icontains": field_search_value})

        return qs.filter(q_list)

    @staticmethod
    def sort(
        qs: QuerySet, fields: List[Any], filters: Dict[str, Any], force_lower: bool
    ) -> QuerySet:
        """
        Apply ordering to a queryset based on the order[{field}][column] column request params.
        """
        orders = []

        for o in range(len(fields)):
            order_index = filters.get(f"order[{o}][column]")
            if order_index is not None:
                field = fields[int(order_index)]
                try:
                    django_field = qs.model._meta.get_field(field)
                except FieldDoesNotExist:
                    django_field = None

                if force_lower and django_field and isinstance(django_field, CharField):
                    field = Lower(field)
                else:
                    field = F(field)

                ordered_field = (
                    field.desc(nulls_last=True)
                    if filters.get(f"order[{o}][dir]") == "desc"
                    else field.asc(nulls_last=True)
                )
                orders.append(ordered_field)

        if orders:
            qs = qs.order_by(*orders)

        return qs

    @staticmethod
    def count(qs: QuerySet) -> QuerySet:
        return qs.count()


class TableListProcessor:
    @staticmethod
    def filter(data: List, fields: List[str], filters: Dict[str, Any]) -> List:
        """
        Apply filtering to a list based on the search[value] request params and
        columns[{field}][search][value] column request params.
        """

        global_search_value = filters.get("search[value]")

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
            for o, field in enumerate(fields):
                field_search_value = filters.get(f"columns[{o}][search][value]")
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

    @staticmethod
    def sort(
        data: List, fields: List[str], filters: Dict[str, Any], force_lower: bool
    ) -> List:
        """
        Apply ordering to a list based on the order[{field}][column] column request params.
        """

        def conditionally_apply_lower(v):
            if force_lower and isinstance(v, str):
                return v.lower()
            return v

        for o in range(len(fields)):
            order_index = filters.get(f"order[{o}][column]")
            if order_index is not None:
                field = fields[int(order_index)]
                direction = filters.get(f"order[{o}][dir]")
                data = sorted(
                    data,
                    key=lambda x: conditionally_apply_lower(x[field]),
                    reverse=direction == "desc",
                )

        return data

    @staticmethod
    def count(data: List) -> int:
        return len(data)


class TableDataProcessorMixin:
    _meta: Type[Any]

    @classmethod
    def get_data_processor(cls, data):
        if isinstance(data, QuerySet):
            return TableQuerysetProcessor
        elif isinstance(data, Iterable):
            return TableListProcessor

        raise Exception("data must be either a queryset or a list")

    @classmethod
    def filter(
        cls, data: Union[QuerySet, List], filters: Dict[str, Any]
    ) -> Union[List, QuerySet]:
        fields = list(cls._meta.columns)
        return cls.get_data_processor(data).filter(data, fields, filters)

    @classmethod
    def sort(
        cls,
        data: Union[QuerySet, List],
        filters: Dict[str, Any],
    ) -> Union[List, QuerySet]:
        force_lower = cls._meta.force_lower
        fields = list(cls._meta.columns)
        return cls.get_data_processor(data).sort(data, fields, filters, force_lower)

    @classmethod
    def count(cls, data: Union[QuerySet, List]):
        return cls.get_data_processor(data).count(data)

    @staticmethod
    def apply_paginator(
        data: Union[QuerySet, List], start: int, length: int
    ) -> Tuple[Page, int]:
        paginator = Paginator(data, length)
        page_number = (int(start) / int(length)) + 1
        return paginator.get_page(page_number), paginator.count
