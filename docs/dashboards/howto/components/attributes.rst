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

``defer_url``

A str or callable which acts as ``defer`` but calling after initial load to a specific url.


``def_FOO_value / def_FOO_defer``

Declaring a function on a dashboard where FOO is the attribute of the defined component
is an alternative to providing a value or defer for example:

::

    from wildcoeus.dashboards.component import Text
    from wildcoeus.dashboards.dashboard import Dashboard

    class ExampleDashboard(Dashboard):
        value_from_method = Text()
        defer_from_method = Text()

        def get_value_from_method_value(self, **kwargs):
            return "I am defined as a FOO value."

        def get_defer_from_method_defer(self, **kwargs):
            request = kwargs["request"]
            return f"hello {request.user} I am defined as a FOO defer."

It's also possible to define your components via  ``__init__`` if you require more granular control of
the components, for details on this see :doc:`dynamic dashboards <../dynamic>`


Optional
++++++++

``template``

While each of the include components has a template, it's possible to provide your own and component
by component basic.

::

    one = Text(template="custom/template/one.html")

TODO BELOW

``depenedents``

``icon``

``css_classes``

``grid_css_classes``

``poll_rate``

``trigger_on``

``CTA``
