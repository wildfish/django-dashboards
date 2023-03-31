from django.core.exceptions import PermissionDenied

import pytest

from dashboards.views import FormComponentView


pytest_plugins = [
    "tests.dashboards.fixtures",
]


def test_get(rf, filter_dashboard):
    request = rf.get("/")
    view = FormComponentView(dashboard_class=filter_dashboard)
    view.setup(request=request, component="filter_component")
    response = view.get(request)

    assert response.status_code == 200
    assert list(response.context_data.keys()) == [
        "component",
        "dashboard",
        "view",
    ]
    assert isinstance(response.context_data["dashboard"], filter_dashboard)


def test_get_template_names__partial(rf, filter_dashboard):
    view = FormComponentView(dashboard_class=filter_dashboard)
    view.setup(rf.get("/dash/app1/TestFilterDashboard/component_1/"))

    assert view.get_template_names() == ["dashboards/components/partial.html"]


@pytest.mark.django_db
def test_admin_only_dashboard__no_permission(rf, admin_dashboard, user):
    request = rf.get("/")
    request.user = user
    request.htmx = False
    view = FormComponentView(dashboard_class=admin_dashboard)
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
    view = FormComponentView(dashboard_class=admin_dashboard)
    view.setup(request, component="component_1")

    assert view.dispatch(request).status_code == 200


def test_post(filter_dashboard, rf):
    request = rf.post("/dash/app1/TestFilterDashboard/component_1/", {"country": "two"})
    view = FormComponentView(dashboard_class=filter_dashboard)
    view.setup(request=request, component="filter_component")
    response = view.post(request)

    assert response.status_code == 200


def test_post_ajax(filter_dashboard, rf, snapshot):
    request = rf.post("/dash/app1/TestFilterDashboard/component_1/", {"country": "two"})
    request.headers = {"x-requested-with": "XMLHttpRequest"}
    view = FormComponentView(dashboard_class=filter_dashboard)
    view.setup(request=request, component="filter_component")
    snapshot.assert_match(view.post(request).content)
    response = view.post(request)

    assert response.status_code == 200
