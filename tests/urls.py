from django.urls import include, path


urlpatterns = [
    path("", include("wildcoeus.pipelines.urls")),
    path("", include("wildcoeus.dashboards.urls")),
]
