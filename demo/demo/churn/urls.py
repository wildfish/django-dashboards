from django.urls import path

from demo.churn.views import ScenarioEditView, ScenarioListView, ScenarioRowView


urlpatterns = [
    path(
        "scenario/",
        ScenarioListView.as_view(),
        name="scenario_list",
    ),
    path(
        "scenario/row/<int:pk>/",
        ScenarioRowView.as_view(),
        name="scenario_row",
    ),
    path(
        "scenario/edit/<int:pk>/",
        ScenarioEditView.as_view(),
        name="scenario_edit",
    ),
]

app_name = "churn"
