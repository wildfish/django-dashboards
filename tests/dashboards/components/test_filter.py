from django.urls import reverse
from django import forms
import pytest

from dashboards.component.filters import Filter
from dashboards.forms import DashboardForm
from tests.utils import render_component_test

pytest_plugins = [
    "tests.dashboards.fixtures",
]

class TestFilter(DashboardForm):
    filter_field = forms.CharField()

@pytest.mark.parametrize("htmx", [True, False])
def test_filter_component__renders_value(dashboard, htmx, rf, snapshot):
    form_instance = TestFilter()  # Create an instance of the form
    component = Filter(form=form_instance, model=None, method="get")
    component.dashboard = dashboard
    component.key = "test"

    # Ensure that the Filter component is added to the dashboard's components
    dashboard.components = [component]

    context = Context(
        {
            "component": component,
            "request": rf.get("/"),
        }
    )

    snapshot.assert_match(render_component_test(context, htmx=htmx))
@pytest.mark.parametrize("method", ["get", "post"])
def test_filter_component__get_value(dashboard, method, rf):
    component = Filter(form=TestFilter, model=None, method=method, dependents=["component_1"])
    component.dashboard = dashboard
    component.key = "test"
    request = rf.get("/")
    value = component.get_value(request)

    assert isinstance(value["form"], TestFilter)
    assert value["method"] == method
    assert value["dependents"] == ["component_1"]
    assert value["action"] == component.get_submit_url()

def test_filter_component__get_submit_url(dashboard):
    component = Filter(form=TestFilter, model=None)
    component.dashboard = dashboard
    component.key = "test"

    assert component.get_submit_url() == reverse(
        "dashboards:filter_component",
        args=[dashboard._meta.app_label, dashboard.class_name(), "test"],
    )

def test_filter_component__get_submit_url__specified(dashboard):
    component = Filter(form=TestFilter, model=None, submit_url="/submit-me/")
    component.dashboard = dashboard
    component.key = "test"

    assert component.get_submit_url() == "/submit-me/"

def test_filter_component__get_form_with_get(dashboard, rf):
    component = Filter(form=TestFilter, model=None, method="get")
    component.dashboard = dashboard
    component.key = "test"
    request = rf.get("/?filter_field=value")
    form = component.get_form(request)

    assert isinstance(form, TestFilter)

def test_filter_component__get_form_with_post(dashboard, rf):
    component = Filter(form=TestFilter, model=None, method="post")
    component.dashboard = dashboard
    component.key = "test"
    request = rf.post("/", {"filter_field": "value"})

    form = component.get_form(request)

    assert isinstance(form, TestFilter)

def test_filter_component__get_value_returns_error_on_invalid(dashboard, rf):
    component = Filter(form=TestFilter, model=None, method="get")
    component.dashboard = dashboard
    component.key = "test"
    request = rf.post("/", {})
    form = component.get_form(request)

    assert form.errors == {"filter_field": ["This field is required."]}
