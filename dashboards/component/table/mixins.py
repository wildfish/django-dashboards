from typing import Any, Dict, List, Union

from django.core.exceptions import FieldDoesNotExist
from django.db.models import CharField, F, Q, QuerySet
from django.db.models.functions import Lower


class TableFilterMixin:
    _meta: Any

    @classmethod
    def filter(
        cls, data: Union[QuerySet, List], filters: Dict[str, Any]
    ) -> Union[List, QuerySet]:
        if isinstance(data, QuerySet):
            return cls._queryset_filter(data, filters)
        else:
            return cls._list_filter(data, filters)

    @classmethod
    def _queryset_filter(cls, qs: QuerySet, filters: Dict[str, Any]) -> QuerySet:
        """
        Apply filtering on  a queryset based on the search[value] and
        columns[{field}][search][value] column request params.
        """

        global_search_value = filters.get("search[value]")
        # used to filter out non model fields
        model_fields = [f.name for f in qs.model._meta.get_fields()]

        q_list = Q()
        fields = list(cls._meta.columns.keys())
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

    @classmethod
    def _list_filter(cls, data: List, filters: Dict[str, Any]) -> List:
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
            for o, field in enumerate(cls._meta.columns.keys()):
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


class TableSortMixin:
    _meta: Any

    @classmethod
    def sort(
        cls, data: Union[QuerySet, List], filters: Dict[str, Any]
    ) -> Union[List, QuerySet]:
        if isinstance(data, QuerySet):
            return cls._queryset_sort(data, filters)
        else:
            return cls._list_sort(data, filters)

    @classmethod
    def _queryset_sort(cls, qs: QuerySet, filters: Dict[str, Any]) -> QuerySet:
        """
        Apply ordering to a queryset based on the order[{field}][column] column request params.
        """
        orders = []
        fields = list(cls._meta.columns.keys())

        for o in range(len(fields)):
            order_index = filters.get(f"order[{o}][column]")
            if order_index is not None:
                field = fields[int(order_index)]
                try:
                    django_field = qs.model._meta.get_field(field)
                except FieldDoesNotExist:
                    django_field = None

                if (
                    cls._meta.force_lower
                    and django_field
                    and isinstance(django_field, CharField)
                ):
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

    @classmethod
    def _list_sort(cls, data: List, filters: Dict[str, Any]) -> List:
        """
        Apply ordering to a list based on the order[{field}][column] column request params.
        """

        def conditionally_apply_lower(v):
            if cls._meta.force_lower and isinstance(v, str):
                return v.lower()
            return v

        fields = list(cls._meta.columns.keys())

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


class TableCountMixin:
    Meta: Any

    @classmethod
    def count(cls, data: Union[QuerySet, List]):
        if isinstance(data, QuerySet):
            return cls._queryset_count(data)
        else:
            return cls._list_count(data)

    @staticmethod
    def _list_count(data: List) -> int:
        return len(data)

    @staticmethod
    def _queryset_count(qs: QuerySet) -> QuerySet:
        return qs.count()


class TableMixin(
    TableFilterMixin,
    TableSortMixin,
    TableCountMixin,
):
    pass
