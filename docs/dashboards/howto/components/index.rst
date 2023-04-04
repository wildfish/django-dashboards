Components
==========

A key part of building a dashboard in django-dashboards is components.

Components act as the building blocks of a dashboard with each component an element.

Generally components are added to dashboards as attributes

::

    from dashboards.dashboard import Dashboard
    from dashboards.component import Text
    from dashboards.registry import registry


    class FirstDashboard(Dashboard):
        welcome = Text(value="Welcome to Django Dashboards!")

        class Meta:
            name = "First Dashboard"


    registry.register(FirstDashboard)

django-dashboards comes bundled with a number of predefined components but you can also build your own, use them
dynamically and much more:


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   ./included.rst
   ./attributes.rst
   ./custom.rst
