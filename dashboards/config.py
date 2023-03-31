from typing import Dict, Optional

from django.conf import settings
from django.utils.module_loading import import_string


def merge_css_dictionaries(default_css_classes, css_classes):
    # apply overrides to default dict
    if css_classes and isinstance(css_classes, dict):
        # for each component update the keys defined
        for k, v in css_classes.items():
            if isinstance(default_css_classes[k], dict):
                default_css_classes[k].update(v)
            else:
                default_css_classes[k] = v

    return default_css_classes


class Config:
    @property
    def DASHBOARDS_DEFAULT_PERMISSION_CLASSES(cls) -> list[str]:
        return getattr(
            settings,
            "DASHBOARDS_DEFAULT_PERMISSION_CLASSES",
            ["dashboards.permissions.AllowAny"],
        )

    @property
    def DASHBOARDS_DEFAULT_GRID_CSS(cls) -> str:
        return getattr(
            settings,
            "DASHBOARDS_DEFAULT_GRID_CSS",
            "span-6",
        )

    @property
    def DASHBOARDS_INCLUDE_DASHBOARD_VIEWS(cls) -> bool:
        return getattr(
            settings,
            "DASHBOARDS_INCLUDE_DASHBOARD_VIEWS",
            True,
        )

    @property
    def DASHBOARDS_COMPONENT_CLASSES(cls) -> Dict[str, Optional[Dict[str, str]]]:
        # default css classes
        FORM_CLASSES = {
            "form": "form",
            "table": "table form-table",
            "button": "btn",
        }
        TABLE_CLASSES = {"table": "table"}
        STAT_CLASSES = {
            "stat": "stat",
            "icon": "stat__icon",
            "heading": "stat__heading",
            "text": "stat__text",
        }
        default_css_classes = {
            "Form": FORM_CLASSES,
            "Table": TABLE_CLASSES,
            "BasicTable": TABLE_CLASSES,
            "Stat": STAT_CLASSES,
        }
        # get any overrides from settings
        css_classes = getattr(settings, "DASHBOARDS_COMPONENT_CLASSES", None)
        # merge
        return merge_css_dictionaries(default_css_classes, css_classes)

    @property
    def DASHBOARDS_LAYOUT_COMPONENT_CLASSES(cls) -> Dict[str, Optional[Dict[str, str]]]:
        # get the default dict
        default_css_classes = import_string(
            "dashboards.component.layout.DEFAULT_LAYOUT_COMPONENT_CLASSES"
        )
        # get any overrides from settings
        css_classes = getattr(settings, "DASHBOARDS_LAYOUT_COMPONENT_CLASSES", None)
        # merge
        return merge_css_dictionaries(default_css_classes, css_classes)
