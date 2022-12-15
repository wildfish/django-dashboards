from django.urls import include, path


urlpatterns = [
    path("", include("wildcoeus.dashboards.urls")),
    path("", include("wildcoeus.pipelines.urls")),
]
