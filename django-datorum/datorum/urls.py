from django.urls import path

from datorum.registry import registry

from .views import ComponentView


app_name = "datorum"

urlpatterns = [
    path("", registry.urls),
    path(
        "<str:dashboard>/<str:component>/",
        ComponentView.as_view(),
        name="dashboard_component",
    ),
]
