from django.urls import path

from datorum.registry import registry as dashboard_registry


urlpatterns = [
    path("", dashboard_registry.urls),
]
