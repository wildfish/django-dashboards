========
Settings
========

``WILDCOEUS_DEFAULT_PERMISSION_CLASSES = ["wildcoeus.dashboards.permissions.AllowAny"]``

This allows you to set multiple permissions to be appled to all registered Dashboards, this can be
overridden on a per dashboard basis with ``permissions_classes``.

You can point to one of our built in permissions classes as detailed in :doc:`permissions`  or roll your own.


``WILDCOEUS_GRID_PREFIX = "span"``

TODO - changing


``WILDCOEUS_INCLUDE_DASHBOARD_VIEWS = True``

Set this to ``False`` to disable any registered Dashboards from automatically having a route
to the generic DashboardView added to the urls.

Recommended if you are using only the Graphql Schema or have rolled your own views.





