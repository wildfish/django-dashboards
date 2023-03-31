import pytest

from dashboards.registry import registry


pytest_plugins = [
    "tests.dashboards.fixtures",
]


def test_initial_registry():
    assert registry.items


def test_reset(dashboard):
    assert registry.items
    registry.reset()
    assert registry.items == []


def test_remove(dashboard):
    assert registry.items
    registry.remove(dashboard)
    assert dashboard not in registry.items


def test_get_all_dashboards(dashboard):
    assert registry.items
    assert registry.get_all_items() == registry.items


def test_get_by_classname(dashboard):
    assert registry.get_by_classname("app1", "testdashboard") == dashboard


def test_get_by_classname__not_found__app_name(dashboard):
    with pytest.raises(IndexError):
        assert registry.get_by_classname("app123", "testdashboard")


def test_get_by_classname__not_found__class_name(dashboard):
    with pytest.raises(IndexError):
        assert registry.get_by_classname("app1", "testdashboard1")


def test_get_by_app_label(dashboard):
    class ExtraDashboard(dashboard):  # type: ignore
        class Meta:
            app_label = "new"

    registry.register(ExtraDashboard)

    assert registry.get_by_app_label("new") == [ExtraDashboard]
    assert len(registry.get_by_app_label("app1")) == 7  # the fixture created ones


def test_get_by_slug(dashboard):
    assert registry.get_by_id("app1_testdashboard") == dashboard


def test_get_by_slug__not_found(dashboard):
    with pytest.raises(IndexError):
        assert registry.get_by_id("app1_testdashboard1")


def test_get_urls(dashboard):
    urls = registry.get_urls()
    assert len(urls) == len(registry.items)
