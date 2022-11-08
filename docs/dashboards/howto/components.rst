==========
Components
==========

Attributes
==========

value or defer?
+++++++++++++++

All the included components need to render is either a ``value`` and ``defer`` argument to be passed.
This determines *when* the data is fetched and *where* from

``value``

A value or callable to fetch on initial render.

``defer``

A value or callable which will be fetched after initial load either via an HTMX trigger or a subseuqent API call if
using graphql.

For example:

::

    from wildcoeus.dashboards.component import Text
    from wildcoeus.dashboards.dashboard import Dashboard

    def fetch_something(request)
        return f"Hello {request.user.username}"

    class ExampleDashboard(Dashboard)
        one = Text(value="One")
        two = Text(value="Two")
        three = Text(defer=fetch_something)

In the above example, when the page first loads only the component ``one`` will be displayed.
HTMX triggers are then used to fetch ``two``and ``three``.

In this example note that ``three`` calls a function, this can be any callable that accepts the kwargs

    * request
        *A Django HttpRequest*
    * dashboard
        *A wildcoeus.dashboards.Dashboard instance)*
    * filters
        *A dict containing the GET params of the request*

Optional attributes
+++++++++++++++++++

``template``

While each of the include components has a template, it's possible to provide your own and component
by component basic.

::

    one = Text(template="custom/template/one.html")


``defer_url``

A str or callable which acts as ``defer`` but calling after initial load to a specific url.

TODO BELOW

``depenedents``

``icon``

``css_classes``

``width``

``poll_rate``

``trigger_on``


Included components
===================

Text
++++

TODO example

Stat
++++

TODO example

CTA
+++

TODO example

Progress
++++++++

TODO example

Timeline
++++++++

TODO example

Chart
+++++

TODO example

When rendered with as a Django view without the built-in templates, plotly.js will be applied to the chart component.

Map
+++

TODO example

When rendered with as a Django view without the built-in templates, plotly.js (mapbox) will be applied to the chart component.

Table
+++++

TODO example

When rendered with as a Django view without the built-in templates, datatables.js will be applied to the table component.

BasicTable
++++++++++

Form
++++




Custom components
=================

Custom components can be added to your own codebase by subclassing :code:`Component` or
one of the include components.

# TODO - should we link to a cookbook of various examples - specific css, template overrides etc?

