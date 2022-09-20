from unittest.mock import patch

import pytest


pytest_plugins = [
    "datorum.tests.fixtures",
]

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
          width
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
        "datorum.registry.Registry.get_graphql_dashboards",
        return_value={
            "TestDashboard": dashboard,
            "ComplexDashboard": complex_dashboard,
            "TestAdminDashboard": dashboard,
            "DashboardWithLayout": dashboard_with_layout,
        },
    ):
        return schema


def test_view__dashboards(rf, admin_user, schema_with_dashboards, snapshot):
    query = """
        query getDashboards {
          dashboards {
            Meta {
              name
              slug
            }
            components {
              key
              value
              width
              isDeferred
              renderType
            }
          }
        }
     """

    request = rf.get("/")
    request.user = admin_user

    result = schema_with_dashboards.execute_sync(
        query, context_value={"request": request}
    )
    assert result.errors is None
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
        variable_values={"slug": "not-test-dashboard"},
        context_value={"request": request},
    )
    assert result.errors is None
    snapshot.assert_match(result.data["dashboard"])


def test_view__dashboard__with_layout(rf, admin_user, schema_with_dashboards, snapshot):
    request = rf.get("/")
    request.user = admin_user

    result = schema_with_dashboards.execute_sync(
        DASHBOARD_GQL,
        variable_values={"slug": "test-dashboard"},
        context_value={"request": request},
    )
    assert result.errors is None
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
