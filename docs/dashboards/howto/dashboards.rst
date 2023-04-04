==========
Dashboards
==========

Dashboards are used to define which and how components are shown on the page.
They consist of a list of component objects along with an optional Layout class.

Standard
========

To create a dashboard you must first create a ``dashboards.py`` file in your Django app which
includes a class subclassed from ``Dashboard``:

::

    from dashboards.dashboard import Dashboard


    class DemoDashboard(Dashboard):
        ...

The various components can then be added to the Dashboard object:

::

    from dashboards.dashboard import Dashboard
    from dashboards.component import Text, Chart


    class DemoDashboard(Dashboard):
        text_example = Text(value="Lorem ipsum dolor sit amet, consectetur elit....")
        chart_example = Chart(defer=fetch_chart_data)

Meta
----

Each dashboard may supply a custom ``Meta`` class.  This is combined with the
``Meta`` classes from each of the dashboard base classes to create a merged metaclass
accessible from the ``_meta`` property of the dashboard.
To do this add a class called ``Meta`` as a child of the dashboard object:

::

    from django.utils.translation import gettext_lazy as _
    from dashboards.dashboard import Dashboard
    from dashboards.component import Text, Chart


    class DemoDashboard(Dashboard):
        text_example = Text(value="Lorem ipsum dolor sit amet, consectetur elit....")
        chart_example = Chart(defer=fetch_chart_data)

        class Meta:
            name = _("Demo Dashboard")


The base dashboard meta class contains the following properties:

* ``include_in_menu``: (``bool``): This specifies whether the dashboard should be included in any menus.  Defaults to ``True``
* ``permission_classes`` (``List[BasePermission]``):  This is a list of permissions a user must have in order to view the dashboard.  See Permissions for more details.  If not specified anyone can view the dashboard.
* ``template_name`` (``str``):  If specified this is the template which will be used to render the dashboard.  This allows you to have full control over how the dashboard is displayed.
* ``abstract`` (``bool``): When a dashboard is flagged as abstract it is excluded from the internal dashboard registry and will not appear in any menus. If not specified, this will be set to False even if a parent class is flagged as abstract.
* ``name`` (``str``): A short name for the dashboard to appear in menus etc. If not set the name of the dashboard class is used.
* ``verbose_name`` (``str``): A long name for the dashboard to appear in titles etc.  If not set the ``name`` attribute will be used.
* ``app_label`` (``str``): The name of the app the dashboard is part of, used when looking up the dashboard in the registry and building the automatic urls.  If not set the ``app_label`` is discovered from the django app registry.

Registry
--------

When you create a dashboard you must register it in order for the automatic url routing to be set.

You can do this by passing the ``Dashboard`` class to the dashboard registry ``register`` function

::

    from dashboards.dashboard import Dashboard
    from dashboards.registry import registry


    class DemoDashboard(Dashboard):
        ...


    registry.register(DemoDashboard)

Layout
------
Dashboards by default display components in a 2 column grid but this can be
changed to fit your needs.  This is done by adding a ``Layout``
class to your Dashboard and populating the ``components`` attribute with a
:code:`ComponentLayout` class.  In this you can order your components and position
them on screen using common HTML elements such Divs.

::

    from dashboards.component.layout import Card, ComponentLayout, HTML

    class DemoDashboard(Dashboard):
        text_example = Text(value="Lorem ipsum dolor sit amet, consectetur adipiscing elit....")
        chart_example = Chart(defer=DashboardData.fetch_bar_chart_data)

        class Meta:
            name = "Demo Dashboard"

        class Layout(Dashboard.Layout):
            components = ComponentLayout(
                HTML("<p>Welcome to our demo app</p>"),
                Card("text_example", grid_css_classes="span-12"),
                Card("chart_example", grid_css_classes="span-12")
            )

See :doc:`layout` for further information.


Model Dashboard
===============

Model Dashboards act the same as a standard dashboard but have access to a single Django model.
This allows you to create a single dashboard which changes depending on the object you are viewing.

To create a Model dashboard you extend from ``ModelDashboard`` rather than ``Dashboard``.  You must
then set the queryset where the objects will fetch from.

There are 2 options for this, either:

Set the model in the dashboard meta class.  This will include all objects:

::

    from dashboards.dashboard import ModelDashboard

    class DemoDashboard(ModelDashboard):
        ...

        class Meta:
            name = "Demo Dashboard"
            model = CustomModel

Define a ``get_queryset()`` on the dashboard.  This allows you to filter out any objects
you do not wish to be made available.

::

    from dashboards.dashboard import ModelDashboard

    class DemoDashboard(ModelDashboard):
        ...

        def get_queryset(self):
            return CustomModel.objects.all()

The object is fetched based on the url and is passed into each component as an
``object`` attribute.::

    <str:app_label>/<str:dashboard>/<str:lookup>/

The default for the lookup value will be the `pk` of the object but this can be changed
in the ``Meta`` class::

    from dashboards.dashboard import ModelDashboard

    class DemoDashboard(ModelDashboard):
        ...

        class Meta:
            name = "Demo Dashboard"
            model = CustomModel
            lookup_kwarg: str = "slug_field"
            lookup_field: str = "slug"

Which would create the url pattern::

    <str:app_label>/<str:dashboard>/<str:slug_field>/

This expects that the CustomModel has a slug field.
