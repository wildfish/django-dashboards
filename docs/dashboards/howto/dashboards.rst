==========
Dashboards
==========

Dashboards are used to define which and how components are shown on the page.
They consist of a list of component objects along with an optional Layout class.

Dashboards can live anywhere in your codebase (we tend to use ``dashboards.py`` or a dashboards directory),
they must inherit from Dashboard and be registered:

::

    from dashboards.dashboard import Dashboard
    from dashboards.component import Text
    from dashboards.registry import registry

    class FirstDashboard(Dashboard):
        welcome = Text(value="Welcome to Django Dashboards!")

        class Meta:
            name = "First Dashboard"


    registry.register(FirstDashboard)

Registering your enables the included urls and views used to display the dashboards and fetch deferred components.

Meta
----

As shown above, Meta can be used to change the some configuration propeties including:

* ``include_in_menu``: (``bool``): This specifies whether the dashboard should be included in any menus.  Defaults to ``True``
* ``permission_classes`` (``List[BasePermission]``):  This is a list of permissions a user must have in order to view the dashboard.  See Permissions for more details.  If not specified anyone can view the dashboard.
* ``template_name`` (``str``):  If specified this is the template which will be used to render the dashboard.  This allows you to have full control over how the dashboard is displayed.
* ``abstract`` (``bool``): When a dashboard is flagged as abstract it is excluded from the internal dashboard registry and will not appear in any menus. If not specified, this will be set to False even if a parent class is flagged as abstract.
* ``name`` (``str``): A short name for the dashboard to appear in menus etc. If not set the name of the dashboard class is used.
* ``verbose_name`` (``str``): A long name for the dashboard to appear in titles etc.  If not set the ``name`` attribute will be used.
* ``app_label`` (``str``): The name of the app the dashboard is part of, used when looking up the dashboard in the registry and building the automatic urls.  If not set the ``app_label`` is discovered from the django app registry.

Layout
------
Dashboards by with our default styles applied display components in a 2 column grid but this can be
changed to fit your needs.  This is done by adding a ``Layout``
class to your Dashboard and populating the ``components`` attribute with a
:code:`ComponentLayout` class.  In this you can order your components and position
them on screen using common HTML elements such Divs. You can also nest components inside the layout components:

::

    from dashboards.component.layout import ComponentLayout, HTML, Card, Header
    from dashboards.dashboard import Dashboard
    from dashboards.component import Text
    from dashboards.registry import registry


    class LayoutDashboard(Dashboard):
        welcome = Text(value="Welcome to Django Dashboards!")
        nested_one = Text(value="1")
        nested_two = Text(value="2")

        class Meta:
            name = "First Dashboard"

        class Layout(Dashboard.Layout):
            components = ComponentLayout(
                Header(heading="Hello", size=2),
                HTML("<small>123.00</small>"),
                Card("welcome", grid_css_classes="span-12"),
                Card("nested_one", "nested_two"),
            )


    registry.register(LayoutDashboard)

See :doc:`layout` for further information.


Model Dashboard
---------------

Model Dashboards act the same as a standard dashboard but have access to a single Django model similar to DetailView.
This allows you to create a single dashboard which changes depending on the object you are viewing.

To create a Model dashboard you extend from ``ModelDashboard`` rather than ``Dashboard``.  You must
then set the model/queryset where the objects will fetch from.

There are 2 options for this, either:

Set the model in the dashboard meta class.  This will include all objects:

::

    from dashboards.dashboard import ModelDashboard
    from yourapp.models import CustomModel

    class CustomDashboard(ModelDashboard):
        ...

        class Meta:
            name = "Demo Dashboard"
            model = CustomModel

    registry.register(CustomDashboard)

Define a ``get_queryset()`` on the dashboard.  This allows you to filter out any objects
you do not wish to be made available.

::

    from dashboards.dashboard import ModelDashboard
    from yourapp.models import CustomModel

    class CustomDashboard(ModelDashboard):
        ...

        def get_queryset(self):
            return CustomModel.objects.all()


    registry.register(CustomDashboard)

The object is fetched based on the url and is passed into each component as an
``object`` attribute.::

    <str:app_label>/<str:dashboard>/<str:lookup>/

The default for the lookup value will be the `pk` of the object but this can be changed
in the ``Meta`` class::

    from dashboards.dashboard import ModelDashboard

    class CustomDashboard(ModelDashboard):
        ...

        class Meta:
            name = "Demo Dashboard"
            model = CustomModel
            lookup_kwarg: str = "slug_field"
            lookup_field: str = "slug"

    registry.register(CustomDashboard)

Which would create the url pattern::

    <str:app_label>/<str:dashboard>/<str:slug_field>/

This expects that the CustomModel has a slug field.
