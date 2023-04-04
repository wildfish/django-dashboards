====================
Component Attributes
====================

All components accept a number of attributes which dictate how it looks and functions.

value / defer
++++++++++++++

All components use either a ``value`` or ``defer`` argument to define the data for rendering.
This determines *when* the data is fetched and *where* from

``value``

A value or callable to fetch on initial load.

``defer``

A value or callable which is fetched after initial load via a HTMX trigger.

In the below example, when the page first loads only the components ``one`` and ``two`` are displayed.
HTMX triggers are then used to fetch ``three`` and ``four`` after initial load since they are defined with defer.

::

    from dashboards.component import Text
    from dashboards.dashboard import Dashboard

    def fetch_something(request, *args, **kwargs)
        return f"Hello {request.user.username}"

    class ExampleDashboard(Dashboard)
        one = Text(value="One")
        two = Text(value=fetch_something)
        three = Text(defer=fetch_something)
        four = Text(
            defer=lambda **kwargs: "Deferred text",
        )


In the above example ``one`` returns the text ``One`` but `two``, ``three`` & ``four`` use a
function `fetch_something` as the value.  This can be any callable that accepts kwargs.

Callable
********

Whenever a callable is used it is passed a number of kwargs.

* request
    *A Django HttpRequest*
* dashboard
    *The dashboards.Dashboard instance the component belongs to*
* filters
    *A dict containing any GET/POST params sent during the request*

These can be used to control what is rendered

::

    def get_welcome_message(self, **kwargs):
        request = kwargs["request"]
        if request.user.is_authenticated:
            return f"hello {request.user} welcome to the site."
        else:
            return "You are not logged in"


FOO attributes
**************

Instead of setting a ``value`` or ``defer`` on a component, you can define a function on the Dashboard class instead.

You do this by declaring a ``get_<FOO>_<method>`` function where ``FOO`` is the name of the component and
``method`` is either ``value`` or ``defer`` depending on when you want it rendered

::

    from dashboards.component import Text
    from dashboards.dashboard import Dashboard

    class ExampleDashboard(Dashboard):
        value_from_method = Text()
        defer_from_method = Text()

        def get_value_from_method_value(self, **kwargs):
            return "I am defined as a FOO value."

        def get_defer_from_method_defer(self, **kwargs):
            request = kwargs["request"]
            return f"hello {request.user} I am defined as a FOO defer."

This will assign the value "I am defined as a FOO value." to the ``value_from_method`` component
and "hello <user> I am defined as a FOO defer." to the ``defer_from_method`` component.

****************
Other Attributes
****************

The following attributes are all optional but can be used to alter how a component functions.

defer_url
+++++++++

By default a component renders the ``ComponentView`` during a defer call from HTMX.  \
This is a builtin django-dashboards view which renders just that component to the screen.  If required,
you can create your own version of this.  You do this by creating your own view and providing the url as a
callable to ``defer_url``.  A use case for this is :doc:`Async components <async>` .

::

    ...
    custom_response = Text(
        defer_url=lambda reverse_args: reverse("custom-component-view", args=reverse_args)
    )

defer_loading_template_name
+++++++++++++++++++++++++++

html template to show while the defer function is being called via ajax.

template_name
+++++++++++++

While each components has its own default template, it's possible to provide your own custom template on a component
by component basis.

::

    one = Text(template_name="custom/template/one.html")

cta
+++

A CTA component with a url.  Using this creates an `a href` tag around the component div,
allowing you to link to another page/dashboard from within a dashboard.

::

    from django.urls import reverse_lazy
    from dashboards.component import CTA

    ...
    link = Text(
        value="Find out more!",
        cta=CTA(
            href=reverse_lazy(
                "dashboards:demo_demodashboard"
            ),
        ),
    )

This expects there to be a `DemoDashboard` setup in the `demo` app.

This example generates the following html::

    <a href="/dashboard/demo/demodashboard/">
        <div id="component-link-inner" class="dashboard-component-inner fade-in">
            Find out more!
        </div>
    </a>

icon
++++

A HTML string to render as an icon.

::

    one = Stat(value="Rendered on load", icon='<i class="fa-up"></i>')

``icon`` is provided to the template and can be rendered using ``component.icon``.

Currently only ``Stat`` utilizes ``icon`` but you can easily create your own custom templates to display
them if required.

::

    // customer_component_template.html
    ...
    {% if component.icon %}
        <div>{{ component.icon|safe }}</div>
    {% endif %}
    ...

    // dashboard.py
    ...
    one = Text(template_name="customer_component_template.html", icon='<i class="fa-up"></i>')

css_classes
+++++++++++

Override css classes used in the template.  Components have default values
but these can be changed to match your css file.

**Default Values**

* Form
    "form": "form"

    "table": "table form-table"

    "button": "btn"

* Table / BasicTable
    "table": "table"


* Stat
    "stat": "stat"

    "icon": "stat__icon"

    "heading": "stat__heading"

    "text": "stat__text"

::

    welcome_text = Stat(value=..., css_classes={"stat": "my-stat", "heading": "big-font"})

generates

::

    <div id="welcome_text">
      <table id="welcome_text_table" class="table table-striped nowrap my-table" style="width:100%"></table>
    </div>


grid_css_classes
++++++++++++++++

The css class applied to the component for its grid layout.  This is separate to any `css_classes` defined.
This should match the css grid layout setup in your project.  See layout docs.

::

    welcome_text = Text(value="Hello", grid_css_classes="span-6")

poll_rate
+++++++++

Only works for components using ``defer``.  Frequency that the component is automatically
reloaded (in seconds) using HTMX.  Defaults to never

::

    ...
    def poll_rate(*kwargs):
        // api call to get latest data and return
        return data

    poll_data = Chart(defer=get_data, poll_rate=10)

This example reloads the ``poll_data`` component every 10 seconds, replacing the current component with the new value.

A use case for this is when doing :doc:`Server Sent Events <sse>` .


trigger_on
++++++++++

Only works for components using ``defer``.  Populates the HTMX value for ``hx-trigger`` which
specifies what triggers a AJAX reload of that component.  See https://htmx.org/attributes/hx-trigger/ for more details.

::

    welcome_text = Text(value="Hello", trigger_on="click")

This reloads the ``welcome_text`` component everytime a user clicks on it.

dependents
++++++++++

List of components to refresh after the current component has reloaded.

::

    ...

    def get_chart_data(self, **kwargs):
        filter = kwargs["filter"]

        if "start_date" in filter and filter["start_date"]:
            qs = SalesData.objects.filter(date__gt=filter["start_date"])

        data = convert_qs_table(qs)  // fake function
        return data

    class ExampleDashboard(Dashboard):
        form_example = Form(
            form=FilterForm,
            method="get",
            dependents=["sales_data"],
        )
        sales_data = Table(defer=get_chart_data)


When ``FilterForm`` is submitted the ``sales_data`` component will automatically be reloaded.
See the Form component docs for how forms function.

This example expects the ``FilterForm`` class to have a ``start_date`` field which provides a date.
We use this value to filter down the ``SalesData`` queryset before it is passed to the component to be rendered.
