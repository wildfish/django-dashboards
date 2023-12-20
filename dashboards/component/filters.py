from django_filters import FilterSet, CharFilter

class GenericFilter(FilterSet):

    global_search = CharFilter(
        method='filter_global'
    )

    def filter_global(self, queryset, name, value):

        if isinstance(queryset, list):
            # Filter list data
            return [item for item in queryset 
                if value.lower() in str(item).lower()]
        
        else: 
            # Filter queryset
            return queryset.filter(
                Q(name__icontains=value) |
                Q(email__icontains=value)
            )

    class Meta:
        fields = ['name', 'email']