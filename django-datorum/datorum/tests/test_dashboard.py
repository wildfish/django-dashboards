from django.http.response import Http404

import pytest


pytest_plugins = [
    "datorum.tests.fixtures",
]


def test__get_attributes_order(dashboard, snapshot):
    snapshot.assert_match(dashboard.get_attributes_order())


def test__get_attributes_order__with_parent(complex_dashboard, snapshot):
    snapshot.assert_match(complex_dashboard.get_attributes_order())


def test__get_components__no_layout(dashboard):
    assert dashboard().get_components() == [
        dashboard.component_1,
        dashboard.component_2,
    ]


def test__get_components__with_parent__no_layout(complex_dashboard):
    assert complex_dashboard().get_components() == [
        complex_dashboard.component_3,
        complex_dashboard.component_2,
        complex_dashboard.component_4,
        complex_dashboard.component_5,
        complex_dashboard.component_6,
        complex_dashboard.component_1,
    ]


def test__get_object__missing_kwargs(model_dashboard):
    with pytest.raises(AttributeError):
        model_dashboard().get_object()


@pytest.mark.django_db
def test__get_object__missing_model_404(model_dashboard):
    with pytest.raises(Http404):
        model_dashboard(lookup="1").get_object()


@pytest.mark.django_db
def test__get_object(model_dashboard, user):
    lookup = user.pk
    assert model_dashboard(lookup=lookup).get_object() == user


@pytest.mark.django_db
def test__get_object__change_lookup_field(model_dashboard, user):
    model_dashboard._meta.lookup_field = "username"
    lookup = user.username
    assert model_dashboard(lookup=lookup).get_object() == user


@pytest.mark.django_db
def test__get_object__change_lookup_kwarg(model_dashboard, user):
    model_dashboard._meta.lookup_kwarg = "username"
    model_dashboard._meta.lookup_field = "username"
    lookup = user.username
    assert model_dashboard(username=lookup).get_object() == user


# More tests to add here re layout
