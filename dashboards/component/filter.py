from dashboards.component.base import Component
from django.template.loader import render_to_string
import django_filters

class FilterComponent(Component):
    template_name = "dashboards/components/filter.html"
    filter_class = None
    filter_fields = []
    dependents = []

    def apply_filters(self, queryset, filters):
        if self.filter_class:
            filter_set = self.filter_class(filters, queryset=queryset)
            return filter_set.qs
        return queryset

    def get_rendered_filter_form(self, request):
        if self.filter_class:
            filter_form = self.filter_class(data=request.GET)
            return render_to_string(
                "dashboards/components/filter_form.html",
                {"filter_form": filter_form, "filter_fields": self.filter_fields},
            )
        return ""


class FilterComponentExtended(FilterComponent):
    filter_class = YourModelFilter
    filter_fields = ['price', 'name', 'date_created']  # Specify filter fields based on your model
