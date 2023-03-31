from django.core.exceptions import PermissionDenied
from django.http import Http404

import pytest

from dashboards.views import ComponentView


pytest_plugins = [
    "tests.dashboards.fixtures",
]


def test_get(rf, dashboard):
    request = rf.get("/")
    view = ComponentView(dashboard_class=dashboard)
    view.setup(request=request, component="component_1")
    response = view.get(request)

    assert response.status_code == 200
    assert list(response.context_data.keys()) == ["component", "dashboard", "view"]
    assert isinstance(response.context_data["dashboard"], dashboard)


def test_get__json(rf, dashboard, snapshot):
    request = rf.get("/dash/app1/TestDashboard/component_2/")
    request.htmx = False
    request.headers = {"x-requested-with": "XMLHttpRequest"}
    view = ComponentView(dashboard_class=dashboard)
    view.setup(
        request,
        component="component_2",
    )
    response = view.get(request)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    snapshot.assert_match(response.content)


def test_post(rf, dashboard):
    request = rf.get("/")
    view = ComponentView(dashboard_class=dashboard)
    view.setup(request=request, component="component_1")
    response = view.post(request, {})

    assert response.status_code == 200
    assert list(response.context_data.keys()) == ["component", "dashboard", "view"]
    assert isinstance(response.context_data["dashboard"], dashboard)


def test_post__json(rf, dashboard, snapshot):
    request = rf.get("/dash/app1/TestDashboard/component_2/")
    request.htmx = False
    request.headers = {"x-requested-with": "XMLHttpRequest"}
    view = ComponentView(dashboard_class=dashboard)
    view.setup(
        request,
        component="component_2",
    )
    response = view.post(request, {})

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    snapshot.assert_match(response.content)


def test_get_template_names__partial(rf, dashboard):
    view = ComponentView(dashboard_class=dashboard)
    view.setup(rf.get("/dash/app1/TestDashboard/component_1/"))

    assert view.get_template_names() == ["dashboards/components/partial.html"]


def test_get_partial__htmx__component_found(rf, dashboard):
    request = rf.get("/dash/app1/TestDashboard/component_1/")
    request.htmx = True
    view = ComponentView(dashboard_class=dashboard)
    view.setup(
        request,
        component="component_1",
    )

    actual_dashboard = dashboard(request=request)
    assert (
        view.get_partial_component(actual_dashboard)
        == actual_dashboard.components["component_1"]
    )


def test_get_partial__component_not_found(rf, dashboard):
    request = rf.get("/dash/app1/TestDashboard/component_10/")
    view = ComponentView(dashboard_class=dashboard)
    view.setup(
        request,
        component="component_10",
    )

    with pytest.raises(Http404):
        view.get_partial_component(dashboard(request=request))


def test_get__partial_template(rf, dashboard, snapshot):
    request = rf.get("/dash/app1/TestDashboard/component_2/")
    request.htmx = True
    view = ComponentView(dashboard_class=dashboard)
    view.setup(
        request,
        component="component_2",
    )

    snapshot.assert_match(view.get(request).rendered_content)


@pytest.mark.django_db
def test_model_dashboard__object_is_set(rf, model_dashboard, user, snapshot):
    request = rf.get("/")
    request.htmx = False
    view = ComponentView(dashboard_class=model_dashboard)
    view.setup(request, lookup=user.pk, component="component_1")

    snapshot.assert_match(view.get(request).rendered_content)
    assert view.get(request).context_data["dashboard"].object == user


@pytest.mark.django_db
def test_admin_only_dashboard__no_permission(rf, admin_dashboard, user):
    request = rf.get("/")
    request.user = user
    request.htmx = False
    view = ComponentView(dashboard_class=admin_dashboard)
    view.setup(request, component="component_1")

    with pytest.raises(PermissionDenied):
        view.dispatch(request)


@pytest.mark.django_db
def test_admin_only_dashboard__with_permission(
    rf, django_user_model, admin_dashboard, staff
):
    request = rf.get("/")
    request.user = staff
    request.htmx = False
    view = ComponentView(dashboard_class=admin_dashboard)
    view.setup(request, component="component_1")

    assert view.dispatch(request).status_code == 200
