from importlib import reload

from django.urls import reverse

import pytest


@pytest.fixture()
def swap_include_urls_patterns(settings):
    # set views to false and retrigger urls
    settings.WILDCOEUS_INCLUDE_DASHBOARD_VIEWS = False
    from wildcoeus.dashboards import urls

    reload(urls)

    yield urls.urlpatterns

    # swap back
    settings.WILDCOEUS_INCLUDE_DASHBOARD_VIEWS = True
    from wildcoeus.dashboards import urls

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
    assert reverse("wildcoeus.dashboards:app1_testdashboard") == "/app1/testdashboard/"


def test_include_dashboard_views__true():
    from wildcoeus.dashboards import urls

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
            "app1_testmodeldashboard_dashboard_detail",
        ]
    )
