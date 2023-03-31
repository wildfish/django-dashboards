from unittest.mock import patch

from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.forms import model_to_dict
from django.template import Context

import pytest

from dashboards.component import BasicTable, Table
from dashboards.component.table.mixins import TableFilterMixin, TableSortMixin
from dashboards.component.table.serializers import SerializedTable, TableSerializer
from tests.dashboards.fakes import fake_user
from tests.utils import render_component_test


pytest_plugins = [
    "tests.dashboards.fixtures",
]


@pytest.fixture()
def test_user_serializer__qs():
    class TestTableSerializer(TableSerializer):
        class Meta:
            columns = {"username": "Username", "first_name": "First"}

        def get_queryset(self, *args, **kwargs):
            return User.objects.all()

        @staticmethod
        def get_first_name_value(obj):
            return obj.first_name.upper()

    return TestTableSerializer


@pytest.fixture()
def test_user_serializer__list():
    class TestTableSerializer(TableSerializer):
        class Meta:
            columns = {"username": "Username", "first_name": "First"}

        def get_data(self, *args, **kwargs):
            return [model_to_dict(u) for u in User.objects.all()]

        @staticmethod
        def get_first_name_value(obj):
            return obj["first_name"].upper()

    return TestTableSerializer


@pytest.fixture()
def test_user_serializer__model():
    class TestTableSerializer(TableSerializer):
        class Meta:
            columns = {"username": "Username", "first_name": "First"}
            model = User

    return TestTableSerializer


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

    class TestTableSerializer(TableSerializer):
        class Meta:
            columns = {"username": "Username"}
            queryset = User.objects.all()

    result = TestTableSerializer.filter(data, {"search[value]": "abc"})

    assert list(result) == expected


@pytest.mark.django_db
def test_filter__table_list__global__one_field(dashboard):
    abc = fake_user(username="abc")
    fake_user(username="xyz")

    data = map(model_to_dict, User.objects.all())
    expected = list(map(model_to_dict, [abc]))

    class TestTableSerializer(TableSerializer):
        class Meta:
            columns = {"username": "Username"}

    result = TestTableSerializer.filter(data, {"search[value]": "abc"})

    assert list(result) == expected


@pytest.mark.django_db
def test_filter__table_queryset__global__two_field(dashboard, test_user_serializer__qs):
    abc = fake_user(username="abc")
    xyz = fake_user(username="xyz", first_name="abc")

    data = User.objects.all()
    expected = [abc, xyz]

    result = test_user_serializer__qs.filter(data, {"search[value]": "abc"})

    assert list(result) == expected


@pytest.mark.django_db
def test_filter__table_list__global__two_field(dashboard, test_user_serializer__list):
    abc = fake_user(username="abc")
    xyz = fake_user(username="xyz", first_name="abc")

    data = map(model_to_dict, User.objects.all())
    expected = list(map(model_to_dict, [abc, xyz]))

    result = test_user_serializer__list.filter(data, {"search[value]": "abc"})

    assert list(result) == expected


@pytest.mark.django_db
def test_filter__table_queryset__individual__find_on_username(
    dashboard, test_user_serializer__qs
):
    abc = fake_user(username="abc")
    fake_user(username="xyz", first_name="abc")

    data = User.objects.all()
    expected = [abc]

    result = test_user_serializer__qs.filter(data, {"columns[0][search][value]": "abc"})

    assert list(result) == expected


@pytest.mark.django_db
def test_filter__table_list__individual__find_on_username(
    dashboard, test_user_serializer__list
):
    abc = fake_user(username="abc")
    fake_user(username="xyz", first_name="abc")

    data = map(model_to_dict, User.objects.all())
    expected = list(map(model_to_dict, [abc]))

    result = test_user_serializer__list.filter(
        data, {"columns[0][search][value]": "abc"}
    )

    assert list(result) == expected


@pytest.mark.django_db
def test_filter__table_queryset__individual__find_on_first_name(
    dashboard, test_user_serializer__qs
):
    xyz = fake_user(username="xyz", first_name="abc")

    data = User.objects.all()
    expected = [xyz]

    result = test_user_serializer__qs.filter(data, {"columns[1][search][value]": "abc"})

    assert list(result) == expected


@pytest.mark.django_db
def test_filter__table_list__individual__find_on_first_name(
    dashboard, test_user_serializer__list
):
    xyz = fake_user(username="xyz", first_name="abc")

    data = map(model_to_dict, User.objects.all())
    expected = list(map(model_to_dict, [xyz]))

    result = test_user_serializer__list.filter(
        data, {"columns[1][search][value]": "abc"}
    )

    assert list(result) == expected


@pytest.mark.django_db
def test_count__table_list(dashboard, test_user_serializer__list):
    fake_user(username="xyz", first_name="abc")

    data = list(map(model_to_dict, User.objects.all()))
    expected = User.objects.count()

    result = test_user_serializer__list.filter(
        data, {"columns[1][search][value]": "abc"}
    )

    assert len(result) == expected


@pytest.mark.django_db
def test_count__table_queryset(dashboard, test_user_serializer__qs):
    fake_user(username="xyz", first_name="abc")

    data = User.objects.all()
    expected = data.count()

    result = test_user_serializer__qs.filter(data, {"columns[1][search][value]": "abc"})

    assert result.count() == expected


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
def test_sort__table_queryset(
    filters, force_lower, expected_order, test_user_serializer__qs
):
    one = fake_user(username="abc", first_name="123")
    two = fake_user(username="xyz", first_name="345")
    three = fake_user(username="CBA", first_name="012")

    data = User.objects.all()
    users = [one, two, three]

    test_user_serializer__qs._meta.force_lower = force_lower

    result = test_user_serializer__qs.sort(data, filters)

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
def test_sort__table_list(
    filters, force_lower, expected_order, test_user_serializer__list
):
    one = fake_user(username="abc", first_name="123")
    two = fake_user(username="xyz", first_name="345")
    three = fake_user(username="CBA", first_name="012")

    data = map(model_to_dict, User.objects.all())
    users = list(map(model_to_dict, [one, two, three]))

    test_user_serializer__list._meta.force_lower = force_lower

    result = test_user_serializer__list.sort(data, filters)

    assert list(result) == [users[i] for i in expected_order]


@pytest.mark.django_db
@pytest.mark.parametrize("length", [5, 10, -1])
def test_serializer__queryset(length, test_user_serializer__qs):
    for u in range(0, 11):
        fake_user()

    data = User.objects.all()

    result = test_user_serializer__qs.serialize(filters={"length": length})

    expected_length = length if length > 0 else data.count()
    assert isinstance(result, SerializedTable)
    assert len(result.data) == expected_length
    assert result.draw == 1
    assert result.total == 11
    assert result.filtered == 11


@pytest.mark.django_db
@pytest.mark.parametrize("length", [5, 10, -1])
def test_serializer__model(length, test_user_serializer__model):
    for u in range(0, 11):
        fake_user()

    data = User.objects.all()

    result = test_user_serializer__model.serialize(filters={"length": length})

    expected_length = length if length > 0 else data.count()
    assert isinstance(result, SerializedTable)
    assert len(result.data) == expected_length
    assert result.draw == 1
    assert result.total == 11
    assert result.filtered == 11


@pytest.mark.django_db
@pytest.mark.parametrize("length", [5, 10, -1])
def test_serializer__list(length, test_user_serializer__list):
    for u in range(0, 11):
        fake_user()

    data = list(User.objects.all())

    result = test_user_serializer__list.serialize(filters={"length": length})

    expected_length = length if length > 0 else len(data)
    assert isinstance(result, SerializedTable)
    assert len(result.data) == expected_length
    assert result.draw == 1
    assert result.total == 11
    assert result.filtered == 11


@pytest.mark.django_db
def test_serializer__value_mapping__queryset(test_user_serializer__qs):
    first_names = []
    for u in range(0, 11):
        user = fake_user(first_name=f"name {u}")
        first_names.append(user.first_name.upper())

    result = test_user_serializer__qs.serialize()

    assert [r["first_name"] for r in result.data] == first_names


@pytest.mark.django_db
def test_serializer__value_mapping__list(test_user_serializer__list):
    first_names = []
    for u in range(0, 11):
        user = fake_user(first_name=f"name {u}")
        first_names.append(user.first_name.upper())

    result = test_user_serializer__list.serialize()

    assert [r["first_name"] for r in result.data] == first_names


@pytest.mark.django_db
def test_serializer__sort_and_filter_applied(test_user_serializer__qs):
    for u in range(0, 11):
        fake_user(username=str(u))

    with patch.object(TableSortMixin, "sort") as mock_sort:
        with patch.object(TableFilterMixin, "filter") as mock_filter:
            result = test_user_serializer__qs.serialize()

    assert isinstance(result, SerializedTable)
    assert mock_sort.call_count == 1
    assert mock_filter.call_count == 1


@pytest.mark.django_db
def test_serializer__related_field():
    Permission.objects.create(
        name="Test",
        codename="test",
        content_type=ContentType.objects.get_for_model(User),
    )

    class TestTableSerializer(TableSerializer):
        class Meta:
            columns = {"name": "name", "content_type__name": "ct_name"}

        def get_data(self, *args, **kwargs):
            return Permission.objects.filter(codename="test")

    result = TestTableSerializer.serialize()

    assert isinstance(result, SerializedTable)
    assert result.data[0]["content_type__name"] == "user"


@pytest.mark.django_db
def test_serializer__invalid_fields():
    class TestTableSerializer(TableSerializer):
        class Meta:
            columns = {"x": "name", "y": "ct_name"}
            model = User

    result = TestTableSerializer.serialize()

    assert isinstance(result, SerializedTable)
    assert len(result.data) == 0


@pytest.mark.django_db
def test_serializer__first_as_absolute_url(test_user_serializer__qs):
    fake_user(username="abc", first_name="one")
    fake_user(username="def", first_name="two")

    class ProxyUser(User):
        def get_absolute_url(self):
            return f"/test/{self.username}"

        class Meta:
            app_label = "test"
            proxy = True

    test_user_serializer__qs.get_queryset = lambda *a, **k: ProxyUser.objects.all()
    test_user_serializer__qs._meta.first_as_absolute_url = True

    result = test_user_serializer__qs.serialize()

    assert isinstance(result, SerializedTable)
    assert result.data == [
        {"username": '<a href="/test/abc">abc</a>', "first_name": "ONE"},
        {"username": '<a href="/test/def">def</a>', "first_name": "TWO"},
    ]


@pytest.mark.django_db
def test_no_columns():
    with pytest.raises(ImproperlyConfigured):

        class TestTableSerializer(TableSerializer):
            class Meta:
                model = User
