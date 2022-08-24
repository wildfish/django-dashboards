from django import forms


class DatorumFormMixin:
    def __init__(self, dashboard, dependants=[], *args, **kwargs):
        self.dashboard = dashboard
        self.components = [
            component
            for component in dashboard.get_components()
            if component.key in dependants
        ]
        super().__init__(*args, **kwargs)


class DatorumFilterMixin:
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)


class DatorumForm(DatorumFormMixin, forms.Form):
    pass


class DatorumFilterForm(DatorumFilterMixin, forms.Form):
    pass


class DatorumModelFilterForm(DatorumFilterMixin, forms.ModelForm):
    pass
