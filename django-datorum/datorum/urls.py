from django.urls import path

from datorum.registry import registry

from . import views


app_name = "datorum"

urlpatterns = [
    path("", registry.urls),
    path(
        "<str:app_label>/<str:dashboard>/<str:component>-form/",
        views.FormComponentView.as_view(),
        name="form_component",
    ),
    path(
        "<str:app_label>/<str:dashboard>/component/<str:component>/",
        views.ComponentView.as_view(),
        name="dashboard_component",
    ),
    path(
        "<str:app_label>/<str:dashboard>/<str:lookup>/component/<str:component>/",  # todo: does not work if lookup_kwarg changed
        views.ComponentView.as_view(),
        name="dashboard_component",
    ),
]
