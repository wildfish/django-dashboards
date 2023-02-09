==================
Table Serializers
==================

A ``TableSerializer`` object can be passed to any ``Table`` or ``BasicTable`` component
as a argument for ``value`` or ``defer``:

::

    # dashboards.py
    ...

    class DemoDashboard(Dashboard):
        chart_example_value = Table(value=ExampleTableSerializer)
        chart_example_defer = Table(defer=ExampleTableSerializer)
    ...

Serializers automatically fetch and convert data into a format which can be rendered by the Table component.

Creating a Table Serializer
++++++++++++++++++++++++++++

To create a Table Serializer all you need to do is: subclass ``TableSerializer``, list the columns for the table,
and define your data.

To define your columns you must set a columns attribute on the objects Meta class::

    class ExampleTableSerializer(TableSerializer):
        class Meta:
            columns = {
                "key": "Key",
                "value": "Value",
            }
            ...

The dictionary key should match the name of the key in your datasource, its value is what is
displayed on screen for the table heading.

By default the table will show whatever value is held in the object for the corresponding key.
If you want to change this you can create your own get_FOO_value method on your TableSerializer object::

    class ExampleTableSerializer(TableSerializer):
        class Meta:
            columns = {
                "key": "Key",
                ...
            }
            ...

        @staticmethod
        def get_key_value(obj):
            return f"The Key is: object['key']"

        ...

This example will show the string "The Key is: {key_value}" as the cell value.

Data
****

If your data is stored in a Django model, the defining your
data step becomes really easy.  Either set the Model you're interested in (in the
serializers Meta class), or if you need more control over the queryset you can override the `get_queryset()` method.::


    from wildcoeus.dashboards.component.table import TableSerializer

    class ExampleTableSerializer(TableSerializer):
        class Meta:
            columns = {
                "key": "Key",
                "value": "Value",
            }
            model = ExampleModel
        ...

or::

    from wildcoeus.dashboards.component.table import TableSerializer

    class ExampleTableSerializer(TableSerializer):
        class Meta:
            columns = {
                "key": "Key",
                "value": "Value",
            }

        def get_queryset(self, *args, **kwargs):
            return ExampleModel.objects.filter(value__gt=10)
        ...

Both these examples assume you have a Django model with a ``key`` and ``value`` field::

    class ExampleModel(models.Model):
        key = models.CharField(max_length=25)
        value = models.IntegerField(default=0)
        ...

When overriding ``get_queryset()`` you also have access to the request via the kwargs::

    def get_queryset(self, *args, **kwargs):
        request = kwargs["request"]  # django request object

        qs = ExampleModel.objects.all()
        qs = qs.filter(created_by=request.user)
        qs = qs.order_by("key")

        return qs


If your data doesn't come from a Django model you can still use serializers to prepare your data.
To do this just override the ``get_data`` static method on the serializer e.g.::

    class ExampleTableSerializer(TableSerializer):
        class Meta:
            columns = {
                "key": "Key",
                "value": "Value",
            }

    @staticmethod
    def get_data(**kwargs):
        return [
            {
                "key": f"key_{r}",
                "value": r,
            }
            for r in range(10)
        ]

``get_data`` expects that you return a Python List.

Just like ``get_queryset()`` ``get_data()`` also has access to the request in kwargs.

Filtering, Sorting and Pagination
**********************************

Filtering, Sorting and Pagination is built into the TableSerializer without you needing to do anything.
It simply recognises the parameters passed in from the Table component and how to handle them.  The Table
component uses DataTables under the hood so if you decide to swap this out for something else you will
need to implement your own versions of ``filter()`` and ``sort()`` methods.