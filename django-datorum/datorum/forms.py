from typing import Any, Dict, List

from django import forms
from django.urls import reverse


class DatorumFormMixin:
    def __init__(self, dashboard_class, key, *args, **kwargs):
        self.dashboard_class = dashboard_class
        self.component_key = key
        super().__init__(*args, **kwargs)

    def get_submit_url(self):
        return reverse(
            "datorum:form_component", args=[self.dashboard_class, self.component_key]
        )

    def save(self, **kwargs):
        print("saving the form!!!!")
        return


class DatorumForm(DatorumFormMixin, forms.Form):
    def asdict(self) -> List[Dict[str, Any]]:
        fields = []
        for field in self:
            fields.append(
                {
                    "name": field.name,
                    "label": field.label,
                    "value": field.field.initial or "",
                    "help_text": field.help_text,
                    "id": field.id_for_label,
                    "field_type": field.field.widget.__class__.__name__,
                    "required": field.field.required,
                    "choices": getattr(field.field.widget, "choices", []),
                }
            )

        return fields
