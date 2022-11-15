from unittest.mock import patch

from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.forms import model_to_dict
from django.template import Context

import pytest

from tests.dashboards.fakes import fake_user
from tests.utils import render_component_test
from wildcoeus.dashboards.component import BasicTable, Table
from wildcoeus.dashboards.component.table import TableData
from wildcoeus.dashboards.component.table.mixins import TableFilterMixin, TableSortMixin
from wildcoeus.dashboards.component.table.serializers import TableSerializer


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
def test_filter__table_queryset__global__one_field(dashboard):
    abc = fake_user(username="abc")
    fake_user(username="xyz")

    data = User.objects.all()
    expected = [abc]

    result = TableSerializer(
        filters={"search[value]": "abc"}, fields=["username"]
    ).filter(data)

    assert list(result) == expected


@pytest.mark.django_db
def test_filter__table_list__global__one_field(dashboard):
    abc = fake_user(username="abc")
    fake_user(username="xyz")

    data = map(model_to_dict, User.objects.all())
    expected = list(map(model_to_dict, [abc]))

    result = TableSerializer(
        filters={"search[value]": "abc"}, fields=["username"]
    ).filter(data)

    assert list(result) == expected


@pytest.mark.django_db
def test_filter__table_queryset__global__two_field(dashboard):
    abc = fake_user(username="abc")
    xyz = fake_user(username="xyz", first_name="abc")

    data = User.objects.all()
    expected = [abc, xyz]

    result = TableSerializer(
        filters={"search[value]": "abc"}, fields=["username", "first_name"]
    ).filter(data)

    assert list(result) == expected


@pytest.mark.django_db
def test_filter__table_list__global__two_field(dashboard):
    abc = fake_user(username="abc")
    xyz = fake_user(username="xyz", first_name="abc")

    data = map(model_to_dict, User.objects.all())
    expected = list(map(model_to_dict, [abc, xyz]))

    result = TableSerializer(
        filters={"search[value]": "abc"}, fields=["username", "first_name"]
    ).filter(data)

    assert list(result) == expected


@pytest.mark.django_db
def test_filter__table_queryset__individual__find_on_username(dashboard):
    abc = fake_user(username="abc")
    fake_user(username="xyz", first_name="abc")

    data = User.objects.all()
    expected = [abc]

    result = TableSerializer(
        filters={"columns[0][search][value]": "abc"}, fields=["username", "first_name"]
    ).filter(data)

    assert list(result) == expected


@pytest.mark.django_db
def test_filter__table_list__individual__find_on_username(dashboard):
    abc = fake_user(username="abc")
    fake_user(username="xyz", first_name="abc")

    data = map(model_to_dict, User.objects.all())
    expected = list(map(model_to_dict, [abc]))

    result = TableSerializer(
        filters={"columns[0][search][value]": "abc"}, fields=["username", "first_name"]
    ).filter(data)

    assert list(result) == expected


@pytest.mark.django_db
def test_filter__table_queryset__individual__find_on_first_name(dashboard):
    xyz = fake_user(username="xyz", first_name="abc")

    data = User.objects.all()
    expected = [xyz]
    # if filter_class == TableFilter:
    #     # as if a list of data instead
    #     data = map(model_to_dict, data)
    #     expected = list(map(model_to_dict, expected))

    result = TableSerializer(
        filters={"columns[1][search][value]": "abc"}, fields=["username", "first_name"]
    ).filter(data)

    assert list(result) == expected


@pytest.mark.django_db
def test_filter__table_list__individual__find_on_first_name(dashboard):
    xyz = fake_user(username="xyz", first_name="abc")

    data = map(model_to_dict, User.objects.all())
    expected = list(map(model_to_dict, [xyz]))

    result = TableSerializer(
        filters={"columns[1][search][value]": "abc"}, fields=["username", "first_name"]
    ).filter(data)

    assert list(result) == expected


@pytest.mark.django_db
def test_count__table_list(dashboard):
    fake_user(username="xyz", first_name="abc")

    data = list(map(model_to_dict, User.objects.all()))
    expected = User.objects.count()

    result = TableSerializer(
        filters={"columns[1][search][value]": "abc"}, fields=["username", "first_name"]
    ).count(data)

    assert result == expected


@pytest.mark.django_db
def test_count__table_queryset(dashboard):
    fake_user(username="xyz", first_name="abc")

    data = User.objects.all()
    expected = data.count()

    result = TableSerializer(
        filters={"columns[1][search][value]": "abc"}, fields=["username", "first_name"]
    ).count(data)

    assert result == expected


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
def test_sort__table_queryset(filters, force_lower, expected_order):
    one = fake_user(username="abc", first_name="123")
    two = fake_user(username="xyz", first_name="345")
    three = fake_user(username="CBA", first_name="012")

    data = User.objects.all()
    users = [one, two, three]

    result = TableSerializer(
        filters=filters, fields=["username", "first_name"], force_lower=force_lower
    ).sort(data)

    assert list(result) == [users[i] for i in expected_order]


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
def test_sort__table_list(filters, force_lower, expected_order):
    one = fake_user(username="abc", first_name="123")
    two = fake_user(username="xyz", first_name="345")
    three = fake_user(username="CBA", first_name="012")

    data = map(model_to_dict, User.objects.all())
    users = list(map(model_to_dict, [one, two, three]))

    result = TableSerializer(
        filters=filters, fields=["username", "first_name"], force_lower=force_lower
    ).sort(data)

    assert list(result) == [users[i] for i in expected_order]


@pytest.mark.django_db
@pytest.mark.parametrize("length", [5, 10, -1])
def test_serializer__queryset(length):
    for u in range(0, 11):
        fake_user()

    data = User.objects.all()
    result = TableSerializer(
        fields=["username", "first_name", "is_staff", "last_login", "date_joined"],
        filters={},
    ).serialize(data, start=0, length=length)

    expected_length = length if length > 0 else data.count()
    assert isinstance(result, TableData)
    assert len(result.data) == expected_length
    assert result.draw == 1
    assert result.total == 11
    assert result.filtered == 11


@pytest.mark.django_db
@pytest.mark.parametrize("length", [5, 10, -1])
def test_serializer__list(length):
    for u in range(0, 11):
        fake_user()

    data = list(User.objects.all())
    result = TableSerializer(
        fields=["username", "first_name", "is_staff", "last_login", "date_joined"],
        filters={},
    ).serialize(data, start=0, length=length)

    expected_length = length if length > 0 else len(data)
    assert isinstance(result, TableData)
    assert len(result.data) == expected_length
    assert result.draw == 1
    assert result.total == 11
    assert result.filtered == 11


@pytest.mark.django_db
def test_serializer__sort_and_filter_applied():
    for u in range(0, 11):
        fake_user(username=str(u))

    data = User.objects.all()

    with patch.object(TableSortMixin, "sort") as mock_sort:
        with patch.object(TableFilterMixin, "filter") as mock_filter:
            result = TableSerializer(
                fields=[
                    "username",
                    "first_name",
                    "is_staff",
                    "last_login",
                    "date_joined",
                ],
                filters={"order[0][column]": 0, "order[0][dir]": "desc"},
            ).serialize(data, start=0, length=5)

    assert isinstance(result, TableData)
    assert mock_sort.call_count == 1
    assert mock_filter.call_count == 1


@pytest.mark.django_db
def test_serializer__related_field():
    Permission.objects.create(
        name="Test",
        codename="test",
        content_type=ContentType.objects.get_for_model(User),
    )

    data = Permission.objects.filter(codename="test")
    result = TableSerializer(
        fields=["name", "content_type__name"],
        filters={},
    ).serialize(data=data, start=0, length=5)

    assert isinstance(result, TableData)
    assert result.data[0]["content_type__name"] == "user"


@pytest.mark.django_db
def test_serializer__invalid_fields():
    data = User.objects.all()
    result = TableSerializer(
        fields=["x", "y"],
        filters={},
    ).serialize(data=data, start=0, length=5)

    assert isinstance(result, TableData)
    assert len(result.data) == 0


@pytest.mark.django_db
def test_serializer__first_as_absolute_url():
    fake_user(username="abc", first_name="one")
    fake_user(username="def", first_name="two")

    class ProxyUser(User):
        def get_absolute_url(self):
            return f"/test/{self.username}"

        class Meta:
            app_label = "test"
            proxy = True

    data = ProxyUser.objects.all()
    result = TableSerializer(
        fields=["username", "first_name"],
        filters={},
        first_as_absolute_url=True,
    ).serialize(data=data, start=0, length=5)

    assert isinstance(result, TableData)
    assert result.data == [
        {"username": '<a href="/test/abc">abc</a>', "first_name": "one"},
        {"username": '<a href="/test/def">def</a>', "first_name": "two"},
    ]
