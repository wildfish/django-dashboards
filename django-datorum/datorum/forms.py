from django import forms
from django.urls import reverse


class DatorumFormMixin:
    def __init__(self, dashboard_class, key, *args, **kwargs):
        self.dashboard_class = dashboard_class
        self.component_key = key
        super().__init__(*args, **kwargs)

    def get_submit_url(self):
        return reverse("datorum:form_component", args=[self.dashboard_class, self.component_key])

    def save(self, **kwargs):
        print("saving the form!!!!")
        return


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
