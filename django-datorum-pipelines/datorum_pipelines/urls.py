from django.contrib import admin
from django.urls import path

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
        "<str:slug>/start/",
        views.PipelineStartView.as_view(),
        name="start",
    ),
    path(
        "<str:run_id>/run/",
        views.PipelineRunView.as_view(),
        name="run",
    ),
]
