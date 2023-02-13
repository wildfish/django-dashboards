

Included components
===================

Text
++++

TODO example

Stat
++++

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
        defer=ExampleTableSerializer,
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

Serializer can also be driven directly from Meta.model or defining a get_queryset(obj) method:

::

    class ExampleTableSerializer(TableSerializer):
        class Meta:
            title = "Staff table"
            columns = {
                "id": "ID",
                "first_name": "First Name",
            }
            # model = User

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
        value=ExampleTableSerializer,
    )

Form
++++

The ``Form`` component allows you to add forms to your dashboard.
There are a number of reasons why you may want to do this, such as: adding filtering
or including a form to create an object.

To include a form in your Dashboard simple add a ``Form`` component and pass
a ``DashboardForm`` instance as the ``form`` attribute.  A ``DashboardForm`` is
a normal Django ``Form`` with some additional helper methods.

As well as the form you can pass some optional attributes to control how it functions:

* ``css_classes`` (``dict``): Allows you to change the default css class for ``form``, ``table`` and ``button``
* ``form`` (``DashboardForm``): The Form to render
* ``method`` (``str``): whether to submit the form as a GET or a POST
* ``trigger`` (``str``): what triggers a change.  Can be ``change`` or ``submit``
* ``submit_url`` (``str``): url the form submits to.

::

    from django import forms

    from wildcoeus.dashboards.dashboard import Dashboard
    from wildcoeus.dashboards.component import Form
    from wildcoeus.dashboards.forms import DashboardForm

    class GradeForm(DashboardForm):
        grade = forms.ChoiceField(
            choices=(
                ("all", "All"),
                ("a", "A"),
                ("b", "B"),
                ("c", "C"),
            )
        )

    class DemoDashboard(Dashboard):
        grade_form = Form(
            form=GradeForm,
        )
        ...

This creates a form with a single dropdown with grades form A-C shown.  You can imagine
this being useful as a filter on a table, where students can be filtered based on
their grade.

::

    # dashboards.py
    import random
    from django import forms

    from wildcoeus.dashboards.dashboard import Dashboard
    from wildcoeus.dashboards.component import Form
    from wildcoeus.dashboards.forms import DashboardForm
    from wildcoeus.dashboards.component.table import TableSerializer


    class StudentSerializer(TableSerializer):
        class Meta:
            title = "Students"
            columns = {
                "name": "Name",
                "grade": "Grade",
            }

        @staticmethod
        def get_data(filters, **kwargs):
            students = [
                {
                    "name": f"Student {r}",
                    "grade": random.choice(["a", "b", "c"]),
                }
                for r in range(10)
            ]
            # apply grade filter if available
            if filters and "grade" in filters and filters["grade"] != "all":
                students = list(filter(lambda x: x["grade"] == filters["grade"], students))

            return students


    class GradeForm(DashboardForm):
        grade = forms.ChoiceField(
            choices=(
                ("all", "All"),
                ("a", "A"),
                ("b", "B"),
                ("c", "C"),
            )
        )


    class StudentDashboard(Dashboard):
        grade_form = Form(
            form=GradeForm,
            method="get",
            dependents=["student_table"],
        )
        student_table = Table(value=StudentSerializer)

        class Meta:
            name = "Students"


    registry.register(StudentDashboard)

.. image:: ../_images/components_form_filter.png
   :alt: Form Filter

.. image:: ../_images/components_form_filter_applied.png
   :alt: Form Filter Applied

This example includes everything in the one file but in reality you may want to
split these up into different files to keep your code clean.

You will notice ``dependents`` has been set as an attribute on the ``Form`` component.
If populated, this refreshes all components listed when the form is changed.
In the example above, ``student_table`` will be refreshed when the ``grade_form``
changes.

As well as reloading the component, all form data is automatically passed into
the ``get_data()`` method of the ``TableSerializer`` when the form is changed.
In the example we use this to filter down the students based on the grade selected.

As mentioned you may also want to add a form which creates data.  This can also
be achieved following the same process but with an additional ``save()`` method
on the ``DashboardForm`` to define how to create the data.  When doing this type
of form you will also want to pass ``method="post"`` and ``trigger="submit"`` into
the ``Form`` component

::

    # dashboards.py
    import random
    import copy
    from django import forms

    from wildcoeus.dashboards.dashboard import Dashboard
    from wildcoeus.dashboards.component import Form
    from wildcoeus.dashboards.forms import DashboardForm
    from wildcoeus.dashboards.component.table import TableSerializer


    student_list = [
        {
            "name": f"Student {r}",
            "grade": random.choice(["a", "b", "c"]),
        }
        for r in range(5)
    ]


    class StudentSerializer(TableSerializer):
        class Meta:
            title = "Students"
            columns = {
                "name": "Name",
                "grade": "Grade",
            }

        @staticmethod
        def get_data(filters, **kwargs):
            global student_list

            students = copy.copy(student_list)

            # apply grade filter if available
            if filters and "grade" in filters and filters["grade"] != "all":
                students = list(filter(lambda x: x["grade"] == filters["grade"], students))

            return students


    class GradeForm(DashboardForm):
        grade = forms.ChoiceField(
            choices=(
                ("all", "All"),
                ("a", "A"),
                ("b", "B"),
                ("c", "C"),
            )
        )


    class AddStudentForm(DashboardForm):
        name = forms.CharField(required=True)
        final_grade = forms.ChoiceField(
            choices=(
                ("a", "A"),
                ("b", "B"),
                ("c", "C"),
            )
        )

        def save(self):
            global student_list

            student_list.append(
                {
                    "name": self.cleaned_data["name"],
                    "grade": self.cleaned_data["final_grade"],
                }
            )


    class StudentDashboard(Dashboard):
        grade_form = Form(
            form=GradeForm,
            method="get",
            dependents=["student_table"],
        )
        student_table = BasicTable(value=StudentSerializer)
        add_form = Form(
            form=AddStudentForm,
            method="post",
            trigger="submit",
            css_classes={"btn": "btn btn-primary"},
            dependents=["student_table"]
        )

        class Meta:
            name = "Students"


    registry.register(StudentDashboard)


.. image:: ../_images/components_add_form.png
   :alt: Form Filter Applied


Notice that we are updating a global variable for ``student_list`` in this example
but in real life you could do this with a django Model instead.