from django.urls import path

from datorum.views import DashboardView

from demo.demo_app.dashboards import DemoDashboardOne, DemoDashboardOneVary


urlpatterns = [
    path(
        "",
        DashboardView.as_view(dashboard=DemoDashboardOne),
        name="dashboard-one",
    ),
    path(
        "vary/",
        DashboardView.as_view(dashboard=DemoDashboardOneVary),
        name="dashboard-one-vary",
    ),
    path(
        "div/",
        DashboardView.as_view(
            dashboard=DemoDashboardOne,
            template_name="datorum/as_div.html",
        ),
        name="dashboard-one-div",
    ),
    path(
        "custom/",
        DashboardView.as_view(
            dashboard=DemoDashboardOne,
            template_name="demo/custom.html",
        ),
        name="dashboard-one-custom",
    ),
]

app_name = "demo_app"
