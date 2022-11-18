from django.urls import include, path

from wildcoeus.dashboards import config, views
from wildcoeus.dashboards.registry import registry


app_name = "wildcoeus.dashboards"

COMPONENT_PATTERN = "<str:app_label>/<str:dashboard>/component/<str:component>/"
COMPONENT_OBJECT_PATTERN = (
    "<str:app_label>/<str:dashboard>/<str:lookup>/component/<str:component>/"
)
FORM_COMPONENT_PATTERN = "<str:app_label>/<str:dashboard>/<str:component>-form/"

urlpatterns = []

if config.Config().WILDCOEUS_INCLUDE_DASHBOARD_VIEWS:
    urlpatterns += [
        path("", include(registry.urls)),
    ]

urlpatterns += [
    path(
        FORM_COMPONENT_PATTERN,
        views.FormComponentView.as_view(),
        name="form_component",
    ),
    path(
        COMPONENT_PATTERN,
        views.ComponentView.as_view(),
        name="dashboard_component",
    ),
    path(
        COMPONENT_OBJECT_PATTERN,  # todo: does not work if lookup_kwarg changed
        views.ComponentView.as_view(),
        name="dashboard_component",
    ),
]
