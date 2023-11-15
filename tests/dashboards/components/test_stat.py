from datetime import date, timedelta

from django.contrib.auth.models import User
from django.db.models import Count
from django.template import Context

import pytest

from dashboards.component.stat import Stat, StatData, StatSerializer
from dashboards.component.stat.serializers import (
    StatDateChangeSerializer,
    StatSerializerData,
)
from tests.dashboards.fakes import fake_user
from tests.utils import render_component_test


pytest_plugins = [
    "tests.dashboards.fixtures",
]


@pytest.fixture()
def test_user_serializer():
    class TestStatSerializer(StatSerializer):
        class Meta:
            annotation_field = "id"
            annotation = Count
            model = User
            title = "Users"
            unit = "People"

    return TestStatSerializer


@pytest.fixture()
def test_user_date_serializer():
    class TestStatDateSerializer(StatDateChangeSerializer):
        class Meta:
            annotation_field = "id"
            annotation = Count
            model = User
            title = "Users"
            unit = "People"
            date_field_name = "date_joined"
            previous_delta = timedelta(days=7)

    return TestStatDateSerializer


@pytest.mark.parametrize(
    "component_kwargs",
    [
        {"value": StatData(text="100%", sub_text="increase")},
        {"defer": lambda **k: StatData(text="100%", sub_text="increase")},
        {
            "value": StatData(
                text="100%", sub_text="increase", change_by=1.0, change_by_text="Change"
            )
        },
    ],
)
@pytest.mark.parametrize("htmx", [True, False])
def test_stat_component__renders_value(component_kwargs, dashboard, htmx, rf, snapshot):
    component = Stat(**component_kwargs)
    component.dashboard = dashboard
    component.key = "test"
    context = Context(
        {
            "component": component,
            "request": rf.get("/"),
        }
    )

    snapshot.assert_match(render_component_test(context, htmx=htmx))


@pytest.mark.parametrize("htmx", [True, False])
@pytest.mark.django_db
def test_stat_component__renders_value__with_serializer(
    dashboard, test_user_serializer, htmx, rf, snapshot
):
    component = Stat(value=test_user_serializer)
    component.dashboard = dashboard
    component.key = "test"
    context = Context(
        {
            "component": component,
            "request": rf.get("/"),
        }
    )

    snapshot.assert_match(render_component_test(context, htmx=htmx))


@pytest.mark.parametrize("htmx", [True, False])
@pytest.mark.django_db
def test_stat_component__renders_value__with_date_serializer(
    dashboard, test_user_date_serializer, htmx, rf, snapshot
):
    component = Stat(defer=test_user_date_serializer)
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
def test_serializer__count(test_user_serializer):
    for u in range(0, 11):
        fake_user()

    data = User.objects.all()

    result = test_user_serializer.serialize()

    assert isinstance(result, StatSerializerData)
    assert result.value == data.count()
    assert result.title == "Users"
    assert result.unit == "People"


@pytest.mark.django_db
def test_serializer__with_dates(test_user_date_serializer):
    for u in range(0, 5):
        fake_user()

    for u in range(0, 5):
        fake_user(date_joined=date(2022, 6, 21))

    result = test_user_date_serializer.serialize()

    assert isinstance(result, StatSerializerData)
    assert result.value == 10
    assert result.previous == 5
    assert result.change == 100.0
    assert result.title == "Users"
    assert result.unit == "People"
