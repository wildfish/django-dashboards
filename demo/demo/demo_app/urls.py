from django.urls import path

from datorum.views import DashboardView

from demo.demo_app import dashboards


urlpatterns = [
    path(
        "",
        DashboardView.as_view(dashboard_class=dashboards.DemoDashboardOne),
        name="dashboard-one",
    ),
    path(
        "vary/",
        DashboardView.as_view(dashboard_class=dashboards.DemoDashboardOneVary),
        name="dashboard-one-vary",
    ),
    path(
        "div/",
        DashboardView.as_view(dashboard_class=dashboards.DemoDashboardOneDiv),
        name="dashboard-one-div",
    ),
    path(
        "custom/",
        DashboardView.as_view(
            dashboard_class=dashboards.DemoDashboardOneCustom,
        ),
        name="dashboard-one-custom",
    ),
    path(
        "admin_only/",
        DashboardView.as_view(dashboard_class=dashboards.DemoDashboardAdmin),
        name="dashboard-admin",
    ),
]

app_name = "demo_app"
