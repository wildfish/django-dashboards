from django.urls import resolve

import pytest

from dashboards.menus.menu import (
    DashboardMenu,
    DashboardMenuItem,
    Menu,
    MenuItem,
    make_dashboard_item,
)


pytestmark = pytest.mark.django_db(reset_sequences=True)
pytest_plugins = [
    "tests.dashboards.fixtures",
]


def nested_menu_item():
    grandchildren = [
        MenuItem(title="Item 1.1.1", url="/"),
        MenuItem(title="Item 1.1.2", url="/", children=[]),
    ]

    children = [
        MenuItem(title="Item 1.1", url="/", children=grandchildren),
        MenuItem(title="Item 1.2", url="/"),
        MenuItem(title="Item 1.3", url="/"),
    ]

    menu_item = MenuItem(title="Item 1", url="/", children=children)

    return menu_item


@pytest.fixture
def menu():
    class MenuTest(Menu):
        name = "MenuTest"

        @classmethod
        def get_items(cls, obj=None):
            grandchildren = [
                MenuItem(title="Item 1.1.1", url="/", children=[]),
                MenuItem(title="Item 1.1.2", url="/", children=[]),
            ]

            children = [
                MenuItem(title="Item 1.1", url="/", children=grandchildren),
                MenuItem(title="Item 1.2", url="/"),
                MenuItem(title="Item 1.3", url="/"),
            ]

            parent = [
                MenuItem(title="Item 1", url="/", children=children),
                MenuItem(title="Item 2", url="/", check_func=lambda r: 1 == 2),
            ]

            return parent

    return MenuTest


@pytest.mark.parametrize(
    "check_func, result",
    [
        (lambda r: 1 == 2, False),
        (lambda r: 1 == 1, True),
    ],
)
def test_menu_item__check(check_func, result, user, rf):
    request = rf.get("/")
    request.user = user
    menu_item = MenuItem(title="test", url="/", check_func=check_func)
    menu_item.check(request)
    assert menu_item.visible is result


def test_dashboard_menu_item__check__visible_false(admin_dashboard, user, rf):
    request = rf.get("/")
    request.user = user
    menu_item = DashboardMenuItem(title="test", url="/", dashboard=admin_dashboard)
    menu_item.check(request)
    assert menu_item.visible is False


def test_dashboard_menu_item__check__visible_true(admin_dashboard, admin_user, rf):
    request = rf.get("/")
    request.user = admin_user
    menu_item = DashboardMenuItem(title="test", url="/", dashboard=admin_dashboard)
    menu_item.check(request)
    assert menu_item.visible is True


@pytest.mark.parametrize(
    "check_func, result",
    [
        (lambda r: 1 == 2, False),
        (lambda r: 1 == 1, True),
    ],
)
def test_menu_item__render__sets_visible(check_func, result, user, rf):
    request = rf.get("/")
    request.user = user
    menu_item = MenuItem(title="Item 1", url="/", check_func=check_func)
    menu_item.render(request=request)

    assert menu_item.visible is result


def test_menu_item__render__sets_children(user, rf):
    request = rf.get("/")
    request.user = user
    c1 = MenuItem(title="Item 1.1", url="/")
    c2 = MenuItem(title="Item 1.2", url="/", check_func=lambda r: 1 == 2)
    children = [
        c1,
        c2,
    ]
    menu_item = MenuItem(title="Item 1", url="/", children=children)
    menu_item.render(request=request)

    assert len(menu_item.children) == 1  # type: ignore
    assert c1 in menu_item.children  # type: ignore
    assert c2 not in menu_item.children  # type: ignore


def test_menu_item__render__sets_children_when_function(user, rf):
    request = rf.get("/")
    request.user = user

    def make_children(request):
        c1 = MenuItem(title="Item 1.1", url="/")
        c2 = MenuItem(title="Item 1.2", url="/")
        return [c1, c2]

    menu_item = MenuItem(title="Item 1", url="/", children=make_children)
    menu_item.render(request=request)

    assert len(menu_item.children) == 2  # type: ignore


def test_menu_item__render__sets_parent(user, rf):
    request = rf.get("/")
    request.user = user
    c1 = MenuItem(title="Item 1.1", url="/")
    c2 = MenuItem(title="Item 1.2", url="/")
    children = [
        c1,
        c2,
    ]
    menu_item = MenuItem(title="Item 1", url="/", children=children)
    menu_item.render(request=request)

    assert c1.parent == menu_item
    assert c2.parent == menu_item


def test_menu_item__render__sets_selected(admin_dashboard, user, rf):
    url = admin_dashboard.get_absolute_url()
    request = rf.get(url)
    request.user = user
    request.resolver_match = resolve(url)

    menu_item = MenuItem(title="Item 1", url=url)
    menu_item.render(request=request)

    assert menu_item.selected is True


# test open
def test_menu_item__render__sets_open(admin_dashboard, user, rf):
    url = admin_dashboard.get_absolute_url()
    request = rf.get(url)
    request.user = user
    request.resolver_match = resolve(url)

    c1 = MenuItem(title="Item 1.1", url=url)
    children = [c1]
    menu_item = MenuItem(title="Item 1", url="/", children=children)
    menu_item.render(request=request)

    assert menu_item.open is True
    assert c1.selected is True


def test_menu__render(menu, user, rf):
    request = rf.get("/")
    request.user = user
    available_items = menu.render(request)

    assert len(available_items) == 1
    assert len(available_items[0].children) == 3
    assert len(available_items[0].children[0].children) == 2


def test_model_dashboard_menu__get_items(user):
    class TestDashboardMenu(DashboardMenu):
        name = "Test Model Dashboard Menu"
        app_label = "app1"

    menu_items = TestDashboardMenu.get_items(obj=user)

    assert len(menu_items) == 7  # see conftest auto_register


def test_dashboard_menu__get_items(model_dashboard, user):
    class TestDashboardMenu(DashboardMenu):
        name = "Test Dashboard Menu"
        app_label = "app1"

    menu_items = TestDashboardMenu.get_items()

    assert len(menu_items) == 6  # see conftest auto_register
    assert model_dashboard not in [x.dashboard for x in menu_items]


def test_make_dashboard_item(model_dashboard, user):
    menu_item = make_dashboard_item(model_dashboard, obj=user)

    assert menu_item.title == "Test Model Dashboard"
    assert menu_item.url == model_dashboard(object=user).get_absolute_url()
    assert menu_item.dashboard == model_dashboard
    assert menu_item.children is None
