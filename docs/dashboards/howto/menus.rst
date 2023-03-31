=====
Menus
=====

django-dashboards allows you to build menus easily and in code.  It also allows you to
build dashboard menus in only a few lines of code.  It handles the discovery,
url routing and permission checks all for you out the box.

Creating a Menu
---------------

To create a menu, first create a dashboard_menu.py file within your app.
Then build your Menu by subclassing ``Menu`` and adding ``MenuItems`` to it before
register it.

Think of a ``Menu`` object as a top level section within a larger menu
and its items as children or that section.

You add items to the menu by overriding the ``get_items()`` method and returning
a list of ``MenuItem`` objects for that menu.

::

    # example/dashboard_menu.py
    from dashboards.menus.menu import Menu, MenuItem
    from dashboards.menus.registry import menu_registry

    class ExampleMenu(Menu):
        name = "Example Menu"

    @classmethod
    def get_items(cls, obj: Optional[Any] = None):
        items = [
            MenuItem(title="Login", url="/login/")
            MenuItem(title="Logout", url="/logout/")
        ]

    menu_registry.register(ExampleMenu)

This creates a top level Example Menu with child elements (links) for Login and Logout.

You can define as many ``Menu`` objects as you wish as long as they are in a
dashboard_menu.py file and registered.

Menu Item
+++++++++

``MenuItem``  must include a ``title`` and ``url`` parameter which are used when
rendering the menu.

You can optionally provide ``children``.  This should be a list of ``MenuItem``
and allows you to create a nested tree like structure.::

        ....

        @classmethod
        def get_items(cls, obj: Optional[Any] = None):
            child_items = [
                MenuItem(title="Sub Item 1", url="/1/"),
                MenuItem(title="Sub Item 2", url="/2/"),
            ]

            items = [
                MenuItem(title="Top Level", url="/top/", children=child_items)
            ]

You can also provide a ``check_func`` parameter.  This should be a Python callable
which defines if the item should be shown to the user or not.

This function should accept 1 parameter - ``request`` and return either True or False
depending if the item should be shown or not.

::

    ...

    def boss_check(request):
        if request.user.username == "bigBoss":
            return True
        else:
            return False

    class BossMenu(Menu):
        name = "Boss Only"

        @classmethod
        def get_items(cls, obj: Optional[Any] = None):
            items = [
                MenuItem(title="Boss Page", url="/boss/", check_func=boss_check)
            ]

Creating a Dashboard Menu
-------------------------

You can also generate a Menu based on your dashboards in only a few lines of code.

To create this you first need a dashboard_menu.py file in your app.
You can then create the menu by subclassing ``DashboardMenu``, pointing it to your
dashboards app and registering it.

Think of a ``DashboardMenu`` object as a top level section within a menu and
its contents as children.

::

    # example/dashboard_menu.py
    from dashboards.menus.menu import DashboardMenu
    from dashboards.menus.registry import menu_registry

    class ExampleMenu(DashboardMenu):
        name = "Example Menu"
        app_label = "example"


    menu_registry.register(ExampleMenu)

``app_label`` is the important pasrt as it is what links the menu to the dashboards.
This needs to match the app the dashboards are registered against.

The example above assumes you have a dashboard.py file within an example app::

    # example/dashboards.py
    from dashboards.dashboard import Dashboard
    from dashboards.component import Text


    class Dashboard1(Dashboard):
        text_example = Text(value="blah")

        class Meta:
            name = "First Dashboard"
            app_label="example"


    class Dashboard2(Dashboard):
        text_example = Text(value="blah")

        class Meta:
            name = "Second Dashboard"
            app_label="example"


    class Dashboard3(Dashboard):
        text_example = Text(value="blah")

        class Meta:
            name = "Third Dashboard"
            app_label="example"

In this example, Example Menu would contain 3 child items - First Dashboard, Second Dashboard, Third Dashboard.

You can define as many ``DashboardMenu`` objects as you wish and they don't have to all be in the same file.
If for example you have multiple apps, each with their own dashboards.py file, you could have a dashboard_menu.py file
in each app to define the menus.

Model Dashboards
++++++++++++++++

If the Dashboard is a ``ModelDashboard`` it will only be added to the menu if the page
you are viewing has access to the object.

If you want the page to be included in the menu without an object you need
to fetch and add the object manually as part of ``get_items()``.
You can use the helper function ``make_dashboard_item()`` to generate the object to include

::

    # example/dashboard_menu.py
    from dashboards.menus.menu import DashboardMenu, make_dashboard_item
    ...


    class ExampleMenu(DashboardMenu):
        name = "Example Menu"
        app_label = "example"

        @classmethod
        def get_items(cls, obj: Optional[Any] = None):
            example_obj = ExampleModel.objects.get(pk=1)
            items = super().get_items(obj)  # default items
            items.append(
                make_dashboard_item(Dashboard1, example_obj)
            )  # extra menu item for Dashboard1 with example_obj

            return items

This example assumes you have an ``ExampleModel`` model defined as well as ``Dashboard1``
which extends ``ModelDashboard``


Permissions
+++++++++++

Any Permissions assigned to a dashboard are automatically taken into consideration when generating the menu.
So for example if you have the Dashboard::

    class AdminDashboard(Dashboard):
        admin_text = Text(value="Admin Only Text")

        class Meta:
            name = "Admin Only"
            permission_classes = [IsAdminUser]

The link to the Admin Only dashboard would only show if the logged in user
had the ``is_staff`` permission set.

See Dashboard Permissions for more details on how to set dashboard level permissions

Display
-------

To display the menu in your site, call the ``{% dashboard_menus %}`` templatetag
within the html file, then loop through the ``sections`` variable to render the menu.

django-dashboards does not provide any HTML for a menu out the box as it is assumed you want to
control how it looks and feels yourself.  An example of how this could look is::

    // menu.html
    {% load dashboards %}

    <div class="menu">
        {% dashboard_menus %}
        <nav role="navigation">
            <ul class="menu">
              {% for section, items in sections.items %}
                <li class="{% if section == active_section %}active{% endif %}">
                    <a href="#">{{ section }}</a>
                    <ul class="dropdown">
                        {% for item in items %}
                            <li class="{% if item.selected %}active{% endif %}">
                                <a href="{{ item.url }}">{{ item.title }}</a>
                            </li>
                        {% endfor %}
                    </ul>
                </li>
                {% endfor %}
            </ul>
        </nav>
        <hr/>
    </div>

As you can see, first add ``{% load dashboards %}`` and call ``{% dashboard_menus %}`` to
get the menus into context.  This automatically adds a ``sections`` dictionary variable
which holds all the registered menus which we can then loop though.

If you followed the DashboardMenu example above ``sections`` has 1
item - Example Menu with 3 children: First Dashboard, Second Dashboard, Third Dashboard.
