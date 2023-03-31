from django.urls import include, path

from dashboards import config, views
from dashboards.registry import registry


app_name = "dashboards"

DASHBOARD_PATTERN = "<str:app_label>/<str:dashboard>/"
MODEL_DASHBOARD_PATTERN = DASHBOARD_PATTERN + "<str:lookup>/"

COMPONENT_PATTERN = DASHBOARD_PATTERN + "@component/<slug:component>/"
COMPONENT_OBJECT_PATTERN = MODEL_DASHBOARD_PATTERN + "@component/<slug:component>/"

FORM_COMPONENT_PATTERN = DASHBOARD_PATTERN + "<slug:component>/@form/"
FORM_COMPONENT_OBJECT_PATTERN = MODEL_DASHBOARD_PATTERN + "<slug:component>/@form/"

urlpatterns = []

if config.Config().DASHBOARDS_INCLUDE_DASHBOARD_VIEWS:
    urlpatterns += [
        path("", include(registry.urls)),
    ]

urlpatterns += [
    path(
        COMPONENT_PATTERN,
        views.ComponentView.as_view(),
        name="dashboard_component",
    ),
    path(
        COMPONENT_OBJECT_PATTERN,
        views.ComponentView.as_view(),
        name="dashboard_component",
    ),
    path(
        FORM_COMPONENT_PATTERN,
        views.FormComponentView.as_view(),
        name="form_component",
    ),
    path(
        FORM_COMPONENT_OBJECT_PATTERN,
        views.FormComponentView.as_view(),
        name="form_component",
    ),
]
