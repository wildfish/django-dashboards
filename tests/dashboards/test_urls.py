from importlib import reload

from django.urls import NoReverseMatch, resolve, reverse

import pytest


@pytest.fixture()
def swap_include_urls_patterns(settings):
    # set views to false and retrigger urls
    settings.DASHBOARDS_INCLUDE_DASHBOARD_VIEWS = False
    from dashboards import urls

    reload(urls)

    yield urls.urlpatterns

    # swap back
    settings.DASHBOARDS_INCLUDE_DASHBOARD_VIEWS = True
    from dashboards import urls

    reload(urls)


def get_all_pattern_names(urlpatterns):
    pattern_names = []
    for url in urlpatterns:
        sub = getattr(url, "url_patterns", [])
        for s in sub:
            pattern_names.append(s.name)
        name = getattr(url, "name", None)
        if name:
            pattern_names.append(name)
    return pattern_names


def test_include_dashboard_views__default__included(settings):
    assert reverse("dashboards:app1_testdashboard") == "/dash/app1/testdashboard/"


def test_include_dashboard_views__true():
    from dashboards import urls

    pattern_names = get_all_pattern_names(urls.urlpatterns)

    assert all(
        p in pattern_names
        for p in [
            "app1_testdashboard",
            "app1_testfilterdashboard",
            "app1_testadmindashboard",
            "app1_testcomplexdashboard",
            "app1_testdashboardwithlayout",
            "app1_testmodeldashboard_detail",
            "app1_testnometadashboard",  # app1_ even with no meta
            "form_component",
            "dashboard_component",
        ]
    )


def test_include_dashboard_views__false(swap_include_urls_patterns):
    pattern_names = get_all_pattern_names(swap_include_urls_patterns)

    assert not any(
        p in pattern_names
        for p in [
            "app1_testdashboard",
            "app1_testfilterdashboard",
            "app1_testadmindashboard",
            "app1_testcomplexdashboard",
            "app1_testdashboardwithlayout",
            "app1_testmodeldashboard_detail",
            "app1_testnometadashboard",
        ]
    )


def assert_url_roundtrip(url_name, **kwargs):
    url = reverse(url_name, kwargs=kwargs)

    resolved = resolve(url)

    assert f"{resolved.namespace}:{resolved.url_name}" == url_name
    assert resolved.kwargs == kwargs


def test_dashboard_component_named_form___component_view_does_not_clash_with_the_component_form_url():
    assert_url_roundtrip(
        "dashboards:dashboard_component",
        app_label="foo",
        dashboard="bar",
        component="form",
    )


def test_model_dashboard_component_named_form___component_view_does_not_clash_with_the_component_form_url():
    assert_url_roundtrip(
        "dashboards:dashboard_component",
        app_label="foo",
        dashboard="bar",
        lookup="baz",
        component="form",
    )


def test_dashboard_form_named_component___form_view_does_not_clash_with_the_component_url():
    assert_url_roundtrip(
        "dashboards:form_component",
        app_label="foo",
        dashboard="bar",
        component="component",
    )


def test_model_dashboard_form_named_component___form_view_does_not_clash_with_the_component_url():
    assert_url_roundtrip(
        "dashboards:form_component",
        app_label="foo",
        dashboard="bar",
        lookup="baz",
        component="component",
    )


def test_at_is_not_valid_in_form_and_component_names():
    with pytest.raises(NoReverseMatch):
        reverse(
            "dashboards:dashboard_component",
            kwargs={
                "app_label": "foo",
                "dashboard": "bar",
                "component": "@form",
            },
        )

    with pytest.raises(NoReverseMatch):
        reverse(
            "dashboards:dashboard_component",
            kwargs={
                "app_label": "foo",
                "dashboard": "bar",
                "lookup": "baz",
                "component": "@form",
            },
        )

    with pytest.raises(NoReverseMatch):
        reverse(
            "dashboards:form_component",
            kwargs={
                "app_label": "foo",
                "dashboard": "bar",
                "component": "@component",
            },
        )

    with pytest.raises(NoReverseMatch):
        reverse(
            "dashboards:form_component",
            kwargs={
                "app_label": "foo",
                "dashboard": "bar",
                "lookup": "baz",
                "component": "@component",
            },
        )
