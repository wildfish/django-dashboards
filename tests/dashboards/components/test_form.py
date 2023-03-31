from django import forms
from django.template import Context
from django.urls import reverse

import pytest

from dashboards.component import Form
from dashboards.forms import DashboardForm
from tests.utils import render_component_test


pytest_plugins = [
    "tests.dashboards.fixtures",
]


class TestForm(DashboardForm):
    number = forms.ChoiceField(
        choices=(
            ("one", "one"),
            ("two", "two"),
            ("three", "three"),
        )
    )


@pytest.mark.parametrize("htmx", [True, False])
def test_form_component__renders_value(dashboard, htmx, rf, snapshot):
    component = Form(form=TestForm, method="get")
    component.dashboard = dashboard
    component.key = "test"
    context = Context(
        {
            "component": component,
            "request": rf.get("/"),
        }
    )

    snapshot.assert_match(render_component_test(context, htmx=htmx))


@pytest.mark.parametrize("method", ["get", "post"])
def test_form_component__get_value(dashboard, method, rf):
    component = Form(form=TestForm, method=method, dependents=["component_1"])
    component.dashboard = dashboard
    component.key = "test"
    request = rf.get("/")
    value = component.get_value(request)

    assert isinstance(value["form"], TestForm)
    assert value["method"] == method
    assert value["dependents"] == ["component_1"]
    assert value["action"] == component.get_submit_url()


def test_form_component__get_submit_url(dashboard):
    component = Form(form=TestForm)
    component.dashboard = dashboard
    component.key = "test"

    assert component.get_submit_url() == reverse(
        "dashboards:form_component",
        args=[dashboard._meta.app_label, dashboard.class_name(), "test"],
    )


def test_form_component__get_submit_url__specified(dashboard):
    component = Form(form=TestForm, submit_url="/submit-me/")
    component.dashboard = dashboard
    component.key = "test"

    assert component.get_submit_url() == "/submit-me/"


def test_form_component__get_form_with_get(dashboard, rf):
    component = Form(form=TestForm, method="get")
    component.dashboard = dashboard
    component.key = "test"
    request = rf.get("/?number=two")
    form = component.get_form(request)

    assert isinstance(form, TestForm)


def test_form_component__get_form_with_post(dashboard, rf):
    component = Form(form=TestForm, method="post")
    component.dashboard = dashboard
    component.key = "test"
    request = rf.post("/", {"number": "two"})

    form = component.get_form(request)

    assert isinstance(form, TestForm)


def test_form_component__get_value_returns_error_on_invalid(dashboard, rf):
    component = Form(form=TestForm, method="get")
    component.dashboard = dashboard
    component.key = "test"
    request = rf.post("/", {})
    form = component.get_form(request)

    assert form.errors == {"number": ["This field is required."]}


def test_form_component__get_value__no_form_error(dashboard, rf):
    component = Form()
    component.dashboard = dashboard
    component.key = "test"
    request = rf.get("/")

    with pytest.raises(NotImplementedError):
        assert component.get_form(request)
