from django.urls import path

from wildcoeus.dashboards.views import DashboardView
from .dashboards import RepoDashboard

urlpatterns = [
    path("", DashboardView.as_view(dashboard_class=RepoDashboard), name="repo"),
]

app_name = "repos"
