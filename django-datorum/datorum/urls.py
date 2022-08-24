from django.urls import path

from datorum.registry import registry

from . import views


app_name = "datorum"

urlpatterns = [
    path("", registry.urls),
    path(
        "<str:dashboard>/<str:component>-form/",
        views.FormComponentView.as_view(),
        name="form_component",
    ),
    path(
        "<str:dashboard>/<str:component>/",
        views.ComponentView.as_view(),
        name="dashboard_component",
    ),
]
