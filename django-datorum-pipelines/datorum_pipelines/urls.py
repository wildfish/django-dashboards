from django.urls import path
from django.contrib import admin
from datorum.registry import registry

from . import views


admin.autodiscover()

app_name = "datorum_pipelines"

urlpatterns = [
    path(
        "list/",
        views.PipelineListView.as_view(),
        name="list",
    ),
    path(
        "<str:pipeline_id>/start/",
        views.PipelineStartView.as_view(),
        name="start",
    ),
]
