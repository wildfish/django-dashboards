from django.http.response import Http404

import pytest


pytest_plugins = [
    "tests.dashboards.fixtures",
]


def test__get_attributes_order(dashboard, snapshot):
    snapshot.assert_match(dashboard.components.keys())


def test__get_attributes_order__with_parent(complex_dashboard, snapshot):
    snapshot.assert_match(complex_dashboard.components.keys())


def test__get_components__no_layout(dashboard, rf):
    request = rf.get("/")
    assert dashboard(request=request).get_components() == [
        dashboard.components["component_1"],
        dashboard.components["component_2"],
        dashboard.components["component_3"],
    ]


def test__get_components__with_parent__no_layout(complex_dashboard, rf):
    request = rf.get("/")

    assert complex_dashboard(request=request).get_components() == [
        complex_dashboard.components["component_1"],
        complex_dashboard.components["component_2"],
        complex_dashboard.components["component_3"],
        complex_dashboard.components["component_4"],
        complex_dashboard.components["component_5"],
        complex_dashboard.components["component_6"],
        complex_dashboard.components["component_7"],
    ]


def test__get_object__missing_kwargs(model_dashboard, rf):
    request = rf.get("/")
    with pytest.raises(AttributeError):
        model_dashboard(request=request).get_object()


@pytest.mark.django_db
def test__get_object__missing_model_404(model_dashboard, rf):
    request = rf.get("/")
    with pytest.raises(Http404):
        model_dashboard(request=request, lookup="1").get_object()


@pytest.mark.django_db
def test__get_object(model_dashboard, user, rf):
    request = rf.get("/")
    lookup = user.pk
    assert model_dashboard(request=request, lookup=lookup).get_object() == user


@pytest.mark.django_db
def test__get_object__change_lookup_field(model_dashboard, user, rf):
    request = rf.get("/")
    model_dashboard._meta.lookup_field = "username"
    lookup = user.username
    assert model_dashboard(request=request, lookup=lookup).get_object() == user


@pytest.mark.django_db
def test__get_object__change_lookup_kwarg(model_dashboard, user, rf):
    request = rf.get("/")
    model_dashboard._meta.lookup_kwarg = "username"
    model_dashboard._meta.lookup_field = "username"
    lookup = user.username
    assert model_dashboard(request=request, username=lookup).get_object() == user


# More tests to add here re layout
