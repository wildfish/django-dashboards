========
Settings
========

DASHBOARDS_DEFAULT_PERMISSION_CLASSES
====================================


``DASHBOARDS_DEFAULT_PERMISSION_CLASSES = ["dashboards.permissions.AllowAny"]``

Set multiple permissions to be applied to all registered Dashboards, this can be
overridden on a per dashboard basis with ``permissions_classes``.

You can point to one of our built in permissions classes as detailed in :doc:`permissions`  or roll your own.


DASHBOARDS_DEFAULT_GRID_CSS
===========================

``DASHBOARDS_DEFAULT_GRID_CSS = "span-6"``

As most dashbaords will follow a grid layout, this is the default css classes to add to a component. For example if
you were using bootstrap you could set the following.

::

    DASHBOARDS_DEFAULT_GRID_CSS = "pb-4 col-md-6 col-sm-12"


This will be overridden by when setting the grid css on a :doc:`components/attributes` or dashboard :doc:`layout` directly.

DJANGO_DASHBOARDS_DASHBOARD_VIEWS
=================================

``DJANGO_DASHBOARDS_DASHBOARD_VIEWS = True``

Set this to ``False`` to disable any registered Dashboards from automatically having a route
to the generic DashboardView added to the urls.

DASHBOARDS_LAYOUT_COMPONENT_CLASSES
===================================

Change the default classes provided to cards, for example to add the classes ``primary-card`` to all
uses of ``Card``

    DASHBOARDS_LAYOUT_COMPONENT_CLASSES = {
        "Card": {
            "card": "primary-card card",
        }
    }


Default is imported from ``dashboards.component.layout.DEFAULT_LAYOUT_COMPONENT_CLASSES`` and merged with
any changes set via this setting.