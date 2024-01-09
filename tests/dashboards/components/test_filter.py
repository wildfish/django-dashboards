from django.http import QueryDict

import pytest

from dashboards.component.filters import FilterComponent


@pytest.mark.django_db  # If using a database
def test_filtering_non_orm_data(request_with_filters):
    filter_component = FilterComponent()
    filtered_data = filter_component.get_value(request_with_filters)

    expected_data = {
        "char_field": "example",
        "number_field": 42,
        "date_field": "2022-01-01",
        "boolean_field": True,
        "choice_field": "option1",
    }

    assert filtered_data == expected_data


@pytest.fixture
def request_with_filters(request_factory):
    request = request_factory.get("/my-url/")
    request.GET = QueryDict("char_filter=exam&number_filter=42")
    return request
