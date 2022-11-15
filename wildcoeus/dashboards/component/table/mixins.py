from typing import List, Union

from django.db.models import F, Q, QuerySet
from django.db.models.functions import Lower


class TableFilterMixin:
    filters: dict
    fields: list

    def filter(self, data: Union[QuerySet, List]) -> Union[List, QuerySet]:
        if isinstance(data, QuerySet):
            return self._queryset_filter(data)
        else:
            return self._list_filter(data)

    def _queryset_filter(self, qs: QuerySet) -> QuerySet:
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

    def _list_filter(self, data: List) -> List:
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


class TableSortMixin:
    filters: dict
    fields: list
    force_lower: bool

    def sort(self, data: Union[QuerySet, List]) -> Union[List, QuerySet]:
        if isinstance(data, QuerySet):
            return self._queryset_sort(data)
        else:
            return self._list_sort(data)

    def _queryset_sort(self, qs: QuerySet) -> QuerySet:
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

    def _list_sort(self, data: List) -> List:
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


class TableCountMixin:
    def count(self, data: Union[QuerySet, List]):
        if isinstance(data, QuerySet):
            return self._queryset_count(data)
        else:
            return self._list_count(data)

    @staticmethod
    def _list_count(data: List) -> int:
        return len(data)

    @staticmethod
    def _queryset_count(qs: QuerySet) -> QuerySet:
        return qs.count()


class TableMixin(TableFilterMixin, TableSortMixin, TableCountMixin):
    pass
