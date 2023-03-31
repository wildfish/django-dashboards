Components
==========

A key part of building a dashboard in django-dashboards is components.

Components act as the building blocks of a dashboard with each component an element.

Generally components are added to dashboards as attributes

::

    from dashboards.dashboard import Dashboard
    from dashboards.component import Text, Chart


    class DemoDashboard(Dashboard):
        text_example = Text(value="Lorem ipsum dolor sit amet, consectetur elit....")
        chart_example = Chart(defer=fetch_chart_data)

However you can also define your components via  ``__init__`` if you require more granular control,
for details on this see :doc:`dynamic dashboards <../dynamic>`

::

    from dashboards.dashboard import Dashboard
    from dashboards.component import Text

    class DynamicDashboard(Dashboard):
        def __init__(self, request: HttpRequest, *args, **kwargs):
            super().__init__(request=request, *args, **kwargs)

        # Generated components
        for r in range(1, 3):
            self.components[f"dynamic_component_{r}"] = Text(
                value=f"Component {r}")

django-dashboards comes bundled with a number of predefined components but you can also easily build
your own if needs be see :doc:`dynamic dashboards <./custom>`.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   ./included.rst
   ./attributes.rst
   ./custom.rst
