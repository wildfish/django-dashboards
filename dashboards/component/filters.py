import django_filters
from django.db.models import QuerySet

class GenericFilter(django_filters.FilterSet):
    def __init__(self, data, fields, *args, **kwargs):
        self.data = data
        self.fields = fields
        super().__init__(*args, **kwargs)

    def filter(self, queryset, name, value):
        q_objects = self.build_q_objects(value)
        return queryset.filter(Q(*q_objects)) if q_objects else QuerySet()

    def build_q_objects(self, value):
        q_objects = []

        for item in self.data:
            if self.item_matches_fields(item, value):
                q_objects.append(self.build_q_object(item))

        return q_objects

    def item_matches_fields(self, item, value):
        for field in self.fields:
            if not self.field_match(item, field, value):
                return False
        return True

    def build_q_object(self, item):
        q_object = Q()

        for field, field_type in self.fields.items():
            if field_type == 'char':
                q_object &= Q(**{f'{field}__icontains': item[field]})
            elif field_type == 'choice':
                q_object &= Q(**{field: item[field]})
            # Add more conditions based on your data structure and field types

        return q_object

    def field_match(self, item, field, value):
        # Customize this method based on your matching logic for each field type
        # Example: return str(item[field]) == value
        return True
