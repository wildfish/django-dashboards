from django.urls import path

from datorum.views import DashboardView

from demo.demo_app import dashboards
from demo.demo_app.views import NormalView


urlpatterns = [
    path(
        "",
        DashboardView.as_view(dashboard_class=dashboards.DemoDashboardOne),
        name="dashboard-one",
    ),
    path(
        "normal/",
        NormalView.as_view(),
        name="dashboard-normal",
    ),
]

app_name = "demo_app"
