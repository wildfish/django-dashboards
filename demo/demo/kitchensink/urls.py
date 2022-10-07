from django.urls import path

from datorum.views import DashboardView

from demo.kitchensink import dashboards
from demo.kitchensink.views import NormalView


urlpatterns = [
    # Add a dashboard as a specific home page path
    path(
        "",
        DashboardView.as_view(dashboard_class=dashboards.DemoDashboardOne),
        name="dashboard-one",
    ),
    # Add a dashboard as via a normal django view
    path(
        "normal/",
        NormalView.as_view(),
        name="dashboard-normal",
    ),
]

app_name = "kitchensink"
