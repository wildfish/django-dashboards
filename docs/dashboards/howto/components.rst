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
the components, for details on this see :doc:`dynamic dashboards <dynamic>`


Optional attributes
+++++++++++++++++++

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


Included components
===================

Text
++++

TODO example

Stat
++++

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

When rendered with as a Django view without the built-in templates, datatables.js will be applied to the table component.

To make tables easier to add to a component, you can subclass `TableSerializer` and pass
it's `serialize` function directly to defer or value. This will give you a searchable and sortable
table component:

::

    # dashboards.py
    ...
    table_example = Table(
        defer=ExampleTableSerializer.serialize,
    )


::

    # tables.py
    from wildcoeus.dashboards.component.table import TableSerializer

    class ExampleTableSerializer(TableSerializer):
        class Meta:
            title = "Example table"
            columns = {
                "id": "Title",
                "name": "Name",
                "progress": "Progress",
                "gender": "Gender",
                "dob": "DOB",
            }

        @staticmethod
        def get_data(**kwargs):
            return [
                {
                    "id": 1,
                    "name": f"Name",
                    "progress": 1,
                    "gender": "male",
                    "rating": 1,
                    "col": 1,
                    "dob": "19/02/1984",
                }
            ]

Serializer can also be driven directly from Meta.model, Meta.queryset or defining a get_queryset(obj) method:

::

    class ExampleTableSerializer(TableSerializer):
        class Meta:
            title = "Staff table"
            columns = {
                "id": "ID",
                "first_name": "First Name",
            }
            # model = User
            # queryset = User.objects.all()

        @classmethod
        def get_queryset(cls, **kwargs):
            """
            kwargs are passed through from value/defer as above
            """
            return User.objects.filter(is_staff=True)


You can also customise any of the columns in the serializer via `get_FOO_value`:

::

    class ExampleTableSerializer(TableSerializer):
        ...

        @staticmethod
        def get_first_name_value(obj):
            return obj.first_name.upper()

Additional `Table` attributes

* page_size
    * int (default=10) to set the paging size*
* searching/paging/ordering
    * bool (default=True) to enable datatables features*


Additional `TableSerializer` Meta attributes

* first_as_absolute_url
    * bool (default=False) if the model or object has a get_absolute_url use it in the first column.
* force_lower
    * bool (default=True) forces searching and sorting of data to use lower values.


BasicTable
++++++++++

Basic tables work the same as table, with the js, search & sort disabled.

::

    table_example_not_deferred = BasicTable(
        value=ExampleTableSerializer.serialize,
    )

Form
++++

TODO

Custom components
=================

Custom components can be added to your own codebase by subclassing :code:`Component` or
one of the include components.

# TODO - should we link to a cookbook of various examples - specific css, template overrides etc?

