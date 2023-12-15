from dashboards import forms
from dashboards.component.base import Component
import django_filters

class YourModelFilter(django_filters.FilterSet):
    # you Define your filters here according to your fields structure, for example:
    price = django_filters.NumberFilter()
class FilterComponent(Component):
    template_name = "dashboards/components/filter.html"
    filter_class = None
    dependents = []

    def apply_filters(self, queryset, filters):
        if self.filter_class:
            filter_set = self.filter_class(filters, queryset=queryset)
            return filter_set.qs
        return queryset