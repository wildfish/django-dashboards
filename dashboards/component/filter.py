from dashboards.component.base import Component

class FilterComponent(Component):
    filter_class = None
    dependents: List[str]

    def apply_filters(self, queryset, filters):
        if self.filter_class:
            filter_set = self.filter_class(filters, queryset=queryset)
            return filter_set.qs
        return queryset
