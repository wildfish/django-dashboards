from django.urls import path

from demo.kitchensink import dashboards
from demo.kitchensink.views import (
    AsyncComponentView,
    NoTemplateComponentDeferView,
    CustomComponentView,
    NormalView,
    SyncComponentView,
)

from wildcoeus.dashboards.urls import COMPONENT_PATTERN
from wildcoeus.dashboards.views import DashboardView


urlpatterns = [
    # Add a dashboard as a specific home page path
    path(
        "",
        DashboardView.as_view(dashboard_class=dashboards.DemoDashboard),
        name="dashboard-one",
    ),
    # Add a dashboard as via a normal django view
    path(
        "normal/",
        NormalView.as_view(),
        name="dashboard-normal",
    ),
    # Custom defer_url examples
    path(
        "customcomponent/" + COMPONENT_PATTERN,
        CustomComponentView.as_view(),
        name="custom-component",
    ),
    path(
        "customcomponentdefer/" + COMPONENT_PATTERN,
        NoTemplateComponentDeferView.as_view(),
        name="custom-component-defer",
    ),
    path(
        "synccomponent/" + COMPONENT_PATTERN,
        SyncComponentView.as_view(),
        name="sync-component",
    ),
    path(
        "asynccomponent/" + COMPONENT_PATTERN,
        AsyncComponentView.as_view(),
        name="async-component",
    ),
]

app_name = "kitchensink"
