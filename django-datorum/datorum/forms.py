from django import forms


class DatorumFormMixin:
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)


class DatorumFilterForm(DatorumFormMixin, forms.Form):
    pass


class DatorumModelFilterForm(DatorumFormMixin, forms.ModelForm):
    pass
