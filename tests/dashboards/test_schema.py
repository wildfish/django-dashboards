from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser

import pytest


pytest_plugins = [
    "tests.dashboards.fixtures",
]

DASHBOARDS_GQL = """
    query getDashboards {
      dashboards {
        Meta {
          name
          slug
        }
        components {
          key
          value
          isDeferred
          renderType
        }
      }
    }
 """


DASHBOARD_GQL = """
    query getDashboard($slug: String!) {
      dashboard(slug: $slug) {
        Meta {
          name
          slug
          layoutJson
        }
        components {
          key
          value
          isDeferred
          renderType
        }
      }
    }
"""

COMPONENT_GQL = """
    query getComponent($slug: String!, $key: String!) {
      component(slug: $slug, key: $key) {
        value
        isDeferred
      }
    }
"""


@pytest.fixture()
def schema_with_dashboards(schema, dashboard, complex_dashboard, dashboard_with_layout):
    with patch(
        "wildcoeus.dashboards.registry.Registry.get_graphql_dashboards",
        return_value={
            "TestDashboard": dashboard,
            "TestComplexDashboard": complex_dashboard,
            "TestAdminDashboard": dashboard,
            "TestDashboardWithLayout": dashboard_with_layout,
        },
    ):
        return schema


def test_view__dashboards(rf, admin_user, schema_with_dashboards, snapshot):
    request = rf.get("/")
    request.user = admin_user

    result = schema_with_dashboards.execute_sync(
        DASHBOARDS_GQL, context_value={"request": request}
    )
    assert result.errors is None
    snapshot.assert_match(result.data["dashboards"])


def test_view__dashboards__permission(rf, admin_user, schema_with_dashboards, snapshot):
    request = rf.get("/")
    request.user = admin_user

    result = schema_with_dashboards.execute_sync(
        DASHBOARDS_GQL, context_value={"request": request}
    )
    assert result.errors is None
    assert "test-admin-dashboard" in [
        d["Meta"]["slug"] for d in result.data["dashboards"]
    ]
    snapshot.assert_match(result.data["dashboards"])


def test_view__dashboards__no_permission(rf, schema_with_dashboards, snapshot):
    request = rf.get("/")
    request.user = AnonymousUser()

    result = schema_with_dashboards.execute_sync(
        DASHBOARDS_GQL, context_value={"request": request}
    )
    assert result.errors is None
    assert "test-admin-dashboard" not in [
        d["Meta"]["slug"] for d in result.data["dashboards"]
    ]
    snapshot.assert_match(result.data["dashboards"])


def test_view__dashboard(rf, admin_user, schema_with_dashboards, snapshot):
    request = rf.get("/")
    request.user = admin_user

    result = schema_with_dashboards.execute_sync(
        DASHBOARD_GQL,
        variable_values={"slug": "test-dashboard"},
        context_value={"request": request},
    )
    assert result.errors is None
    snapshot.assert_match(result.data["dashboard"])


def test_view__dashboard__not_found(rf, admin_user, schema_with_dashboards, snapshot):
    request = rf.get("/")
    request.user = admin_user

    result = schema_with_dashboards.execute_sync(
        DASHBOARD_GQL,
        variable_values={"slug": "test-not-dashboard"},
        context_value={"request": request},
    )
    assert result.errors is None
    assert result.data == {"dashboard": None}


def test_view__dashboard__with_layout(rf, admin_user, schema_with_dashboards, snapshot):
    request = rf.get("/")
    request.user = admin_user

    result = schema_with_dashboards.execute_sync(
        DASHBOARD_GQL,
        variable_values={"slug": "test-dashboard-with-layout"},
        context_value={"request": request},
    )
    assert result.errors is None
    assert result.data["dashboard"]["Meta"]["layoutJson"]
    snapshot.assert_match(result.data["dashboard"])


def test_view__component__not_deferred(
    rf, admin_user, schema_with_dashboards, snapshot
):
    request = rf.get("/")
    request.user = admin_user

    result = schema_with_dashboards.execute_sync(
        COMPONENT_GQL,
        variable_values={"slug": "test-dashboard", "key": "component_1"},
        context_value={"request": request},
    )
    assert result.errors is None
    snapshot.assert_match(result.data["component"])


def test_view__component__deferred(rf, admin_user, schema_with_dashboards, snapshot):
    request = rf.get("/")
    request.user = admin_user

    result = schema_with_dashboards.execute_sync(
        COMPONENT_GQL,
        variable_values={"slug": "test-dashboard", "key": "component_2"},
        context_value={"request": request},
    )
    assert result.errors is None
    snapshot.assert_match(result.data["component"])


def test_view__component__deferred__not_found(
    rf, admin_user, schema_with_dashboards, snapshot
):
    request = rf.get("/")
    request.user = admin_user

    result = schema_with_dashboards.execute_sync(
        COMPONENT_GQL,
        variable_values={"slug": "test-not-dashboards", "key": "component_2"},
        context_value={"request": request},
    )
    assert result.errors is None
    assert result.data == {"component": None}
