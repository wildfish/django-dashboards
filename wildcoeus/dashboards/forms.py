from typing import Any, Dict, List

from django import forms


class DashboardForm(forms.Form):
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
