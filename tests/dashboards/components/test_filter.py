import pytest
from django.http import HttpRequest
from django.db.models import CharField, Model
from django.core.exceptions import FieldDoesNotExist
from django_filters import FilterSet
from django.forms.widgets import NumberInput
from .. import config
from ..forms import DashboardForm
from ..types import ValueData
from .base import Component, value_render_encoder
from typing import Literal, Union, Type, Dict, Any, List
from dashboards.component.filters import FilterData, TableFilterSet, TableFilterProcessor, Filter

class FakeModel(Model):
    name = CharField(max_length=255)
    age = CharField(max_length=3)

@pytest.fixture
def fake_model_queryset():
    fake_data = [
        {'name': 'John', 'age': '25'},
        {'name': 'Alice', 'age': '30'},
        {'name': 'Bob', 'age': '22'},
    ]
    return FakeModel.objects.bulk_create([FakeModel(**data) for data in fake_data])

def test_table_filter_processor(fake_model_queryset):
    qs = FakeModel.objects.all()
    filters = {'global_search': 'John'}

    # Test filter method
    filtered_qs = TableFilterProcessor.filter(qs, filters)
    assert len(filtered_qs) == 1
    assert filtered_qs[0].name == 'John'

    sorted_qs = TableFilterProcessor.sort(qs, ['name'], filters, force_lower=False)
    assert list(sorted_qs) == sorted(list(qs), key=lambda x: x.name)

    count = TableFilterProcessor.count(qs)
    assert count == len(qs)

def test_filter(fake_model_queryset):
    form_mock = lambda: None
    filter_component = Filter(form=form_mock)
    filter_component.model = FakeModel

    filterset_class = filter_component.get_filterset()
    assert issubclass(filterset_class, FilterSet)
    assert hasattr(filterset_class, 'global_search')

    request_mock = HttpRequest()
    filters = {'global_search': 'John'}
    value = filter_component.get_value(request=request_mock, filters=filters)
    expected_value = FilterData(form={'global_search': 'John'}, dependents=[])
    assert value == expected_value

    data = FakeModel.objects.all()
    filtered_data = Filter.filter_data(data, filters)
    assert list(filtered_data) == list(data.filter(name__icontains='John'))

    sorted_data = Filter.sort_data(data, filters)
    assert list(sorted_data) == sorted(list(data), key=lambda x: x.name)

    count_data = Filter.count_data(data)
    assert count_data == len(data)

    page, total_records = Filter.apply_paginator(data, start=0, length=10)
    assert len(page.object_list) == 3
    assert total_records == len(data)

