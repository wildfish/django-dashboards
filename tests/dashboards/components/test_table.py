from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.template import Context

import pytest

from tests.dashboards.fakes import fake_user
from tests.utils import render_component_test
from wildcoeus.dashboards.component import BasicTable, Table
from wildcoeus.dashboards.component.table import (
    DatatablesQuerysetFilter,
    DatatablesQuerysetSort,
)


pytest_plugins = [
    "tests.dashboards.fixtures",
]


@pytest.mark.parametrize("component_class", [Table, BasicTable])
@pytest.mark.parametrize(
    "component_kwargs",
    [
        {"value": "value"},
        {"defer": lambda **kwargs: "value"},
        {"value": "value", "css_classes": ["a", "b"]},
    ],
)
@pytest.mark.parametrize("htmx", [True, False])
def test_render(component_class, dashboard, component_kwargs, htmx, rf, snapshot):
    component = component_class(**component_kwargs)
    component.dashboard = dashboard
    component.key = "test"
    context = Context(
        {
            "component": component,
            "request": rf.get("/"),
        }
    )

    snapshot.assert_match(render_component_test(context, htmx=htmx))


@pytest.mark.django_db
def test_filter__datatables_queryset__global__one_field(dashboard):
    abc = fake_user(username="abc")
    fake_user(username="xyz")

    result = DatatablesQuerysetFilter(
        filters={"search[value]": "abc"}, fields=["username"]
    ).filter(User.objects.all())

    assert isinstance(result, QuerySet)
    assert list(result) == [abc]


@pytest.mark.django_db
def test_filter__datatables_queryset__global__two_field(dashboard):
    abc = fake_user(username="abc")
    xyz = fake_user(username="xyz", first_name="abc")

    result = DatatablesQuerysetFilter(
        filters={"search[value]": "abc"}, fields=["username", "first_name"]
    ).filter(User.objects.all())

    assert isinstance(result, QuerySet)
    assert list(result) == [abc, xyz]


@pytest.mark.django_db
def test_filter__datatables_queryset__individual__find_on_username(dashboard):
    abc = fake_user(username="abc")
    fake_user(username="xyz", first_name="abc")

    result = DatatablesQuerysetFilter(
        filters={"columns[0][search][value]": "abc"}, fields=["username", "first_name"]
    ).filter(User.objects.all())

    assert isinstance(result, QuerySet)
    assert list(result) == [abc]


@pytest.mark.django_db
def test_filter__datatables_queryset__individual__find_on_first_name(dashboard):
    xyz = fake_user(username="xyz", first_name="abc")

    result = DatatablesQuerysetFilter(
        filters={"columns[1][search][value]": "abc"}, fields=["username", "first_name"]
    ).filter(User.objects.all())

    assert isinstance(result, QuerySet)
    assert list(result) == [xyz]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "filters,force_lower,expected_order",
    [
        ({}, True, [0, 1, 2]),
        ({"order[0][column]": 0}, True, [0, 2, 1]),
        ({"order[0][column]": 1}, True, [2, 0, 1]),
        (
            {"order[0][column]": 0, "order[0][dir]": "desc"},
            True,
            [1, 2, 0],
        ),
        # Not forced to lower
        ({}, False, [0, 1, 2]),  # Does not change
        ({"order[0][column]": 0}, False, [2, 0, 1]),
        ({"order[0][column]": 1}, False, [2, 0, 1]),  # Does not change
        (
            {"order[0][column]": 0, "order[0][dir]": "desc"},
            False,
            [1, 0, 2],
        ),
    ],
)
def test_sort__datatables_queryset(filters, force_lower, expected_order):
    one = fake_user(username="abc", first_name="123")
    two = fake_user(username="xyz", first_name="345")
    three = fake_user(username="CBA", first_name="012")

    sort_class = DatatablesQuerysetSort
    sort_class.force_lower = force_lower

    result = DatatablesQuerysetSort(
        filters=filters, fields=["username", "first_name"]
    ).sort(User.objects.all())

    print(filters)
    users = [one, two, three]
    assert list(result) == [users[i] for i in expected_order]
