from django.urls import include, path


urlpatterns = [
    path("", include("wildcoeus.dashboards.urls")),
]
