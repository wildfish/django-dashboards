from django.template import Context, Template
from django.urls import resolve

import pytest

from dashboards.menus.menu import Menu, MenuItem
from dashboards.menus.registry import menu_registry


pytestmark = pytest.mark.django_db(reset_sequences=True)
pytest_plugins = [
    "tests.dashboards.fixtures",
]


@pytest.fixture
def menu():
    @menu_registry.register
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
                MenuItem(title="Item 1.3", url="/dash/app1/testmodeldashboard/1/"),
            ]

            parent = [
                MenuItem(title="Item 1", url="/", children=children),
                MenuItem(title="Item 2", url="/"),
            ]

            return parent

    return MenuTest


def test_template_tag(model_dashboard, menu, user, rf):
    """
    Ensure the templating works
    """
    dashboard = model_dashboard(object=user)
    url = dashboard.get_absolute_url()

    request = rf.get(url)
    request.user = user
    request.resolver_match = resolve(url)

    menu_registry.discovered = True  # set to True so it doesn't run autodiscover

    out = Template(
        "{% load dashboards %}"
        "{% dashboard_menus %}"
        "{{ active_section }},"
        "{% for item in sections.MenuTest %}"
        "{{ item }},"
        "{% for child in item.children %}"
        "{{ child.title }}{% if child.selected %} (selected){% endif %},"
        "{% for grandchild in child.children %}"
        "{{ grandchild }},"
        "{% endfor %}"
        "{% endfor %}"
        "{% endfor %}"
    ).render(
        Context(
            {
                "request": request,
                "dashboard": dashboard,
            }
        )
    )

    assert (
        out
        == "MenuTest,Item 1,Item 1.1,Item 1.1.1,Item 1.1.2,Item 1.2,Item 1.3 (selected),Item 2,"
    )
