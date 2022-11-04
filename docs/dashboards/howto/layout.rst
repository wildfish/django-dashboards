=================
Dashboard Layouts
=================

Dashboards by default display components in a 2 column grid, but
this can be customized to fit your needs.  This is done using a :code:`ComponentLayout`
which allows you to order components and position them on screen using common
HTML elements such Divs.

ComponentLayout Class
---------------------

:code:`ComponentLayout` is assigned to the :code:`components` element
of the :code:`Layout` class of a :code:`Dashboard` object.

They are initialized with a number of objects, which can be
of type :code:`Components`, :code:`HTMLComponentLayout` or :code:`HTML`.
:code:`Components` reference the component elements in the Dashboard,
:code:`HTMLComponentLayout` is a HTML element wrapper.  These can be nested
which is how complex layouts can be achieved.
:code:`HTML` allow you to add raw HTML within a dashboard.

We can add a custom layout to the example dashboard from the quickstart guide

:code:`demo/mydashboard/dashboards.py`::

    from wildcoeus.dashboards.component.layout import Card, ComponentLayout, HTML

    class DemoDashboard(Dashboard):
        text_example = Text(value="Lorem ipsum dolor sit amet, consectetur adipiscing elit....")
        chart_example = Chart(defer=DashboardData.fetch_bar_chart_data)

        class Meta:
            name = "Demo Dashboard"

        class Layout(Dashboard.Layout):
            components = ComponentLayout(
                HTML("<p>Welcome to our demo app</p>"),
                Card("text_example", width=12),
                Card("chart_example", width=12)
            )

This will render the dashboard with a html paragraph tag, followed by the text_example,
wrapped in a div with card classes (this should be familiar to bootstrap users), and
finally the chart, again wrapped in a div card.

When referencing dashboard components you just need to add the component attribute in a string.
When using custom layouts only components referenced in the layout will be displayed.

This should look similar to the original dashboard with just an extra html element,
this is because the default layout wraps each component in the card div.

.. image:: _images/layout_basic.png
   :alt: Demo Dashboard

This is a very basic example but you can do much more.  Lets now change the layout::

    class Layout(Dashboard.Layout):
        components = ComponentLayout(
            Header(heading="Welcome", size=2),
            HTML("<p>Below is the results from our investigation:</p>"),
            Card(
                HTML("<h1>Chart Example</h1>"),
                Div("chart_example", width=12),
                width=6
            ),
            Card(
                HTML("<h1>Text Example</h1>"),
                Div("text_example", width=12),
                width=6
            ),
            HR(),
            HTML("<p>Please contact us for more information.</p>")
        )

This creates

.. image:: _images/layout_complex.png
   :alt: Demo Dashboard

This is a very simple dashboard with only 2 components but should give you a feel for
what you can create.

HTMLComponentLayout attributes
------------------------------

All :code:`HTMLComponentLayout` objects can accept a number of kwargs.
These vary depending on the element but common to all objects are
:code:`css_classes` and :code:`width`.  In the complex example above
we used the width attribute to lay the divs in the card side by side.
If we had 3 components we could add the extra card and change the width to 4.::

    Card(
        "text_example",
        width=4
    ),

This adds a css class :code:`span-{width}` e.g. :code:`span-4` to the element.
The css grid layout is based on 12 columns.

You can also add extra css classes to your HTMLComponentLayout elements by::

    Div(
        HTML("Lorem ipsum dolor sit amet"),
        css_classes="some-class another-class"
    ),

This generates::

    <div class="span-12 some-class another-class">
      <div class="span-12 ">Lorem ipsum dolor sit amet</div>
    </div>


Component Layout Objects
------------------------

These live in :code:`wildcoeus.dashboards.component.layout`.

**Div**: Simply wraps the contents in a <div>::

    Div(HTML("<p>Please contact us for more information.</p>"), css_classes="more-styles", width=6))


generates::

    <div class="span-6 more-styles">
      <div class="span-12 "><p>Please contact us for more information.</p></div>
    </div>


**Card**: A common layout element used in popular css templates such as Bootstrap::

    Card(HTML("<p>Please contact us for more information.</p>"), width=12, css_classes="more-styles", heading="some title" footer="some footer text" image_url="" actions=[("", "")])

This example would generate the following html::

    <div class="card more-styles">
        <div class="card-header justify-content-between align-items-center">
          <h4 class="header-title">some title</h4>
          <div class="dropdown">
            <a href="#" class="dropdown-toggle arrow-none card-drop" data-bs-toggle="dropdown" aria-expanded="false">
              <i class="mdi mdi-dots-vertical"></i>
            </a>
            <div class="dropdown-menu dropdown-menu-end" style="">
              <a href="http://google.com" class="dropdown-item">Google</a>
            </div>
          </div>
        </div>
        <div class="card-body pt-0">
          <div class="span-12 ">
            <p>Please contact us for more information.</p>
          </div>
        </div>
          <div class="card-footer">some footer text</div>
      </div>

**TabContainer & Tab**: A more complex component but useful when grouping content within a page::

    TabContainer(
        Tab(
            "Tab 1",
            HTML("Lorem ipsum dolor sit amet."),
            width=12,
        ),
        Tab(
            "Tab 2",
            HTML("Please contact us for more information."),
            width=12,
        ),
        width=12,
    ),

Tabs must be wrapped in a TabContainer::

    <div class="span-12 tab-container" x-data="{ tab: 'tab-1' }">
        <ul>
            <li>
              <a :class="{ 'active': tab === 'tab-1' }" x-on:click.prevent="tab = 'tab-1'" href="#" class="active">
                Tab 1
              </a>
            </li>
            <li>
              <a :class="{ 'active': tab === 'tab-2' }" x-on:click.prevent="tab = 'tab-2'" href="#" class="">
                Tab 2
              </a>
            </li>
        </ul>
        <div class="tab-content">
            <div :class="{ 'active show': tab === 'tab-1' }" x-show="tab === 'tab-1'" class="active show" style="">
                <div class="span-12 tab-content">
                  <div class="span-12 ">Lorem ipsum dolor sit amet.</div>
                </div>
            </div>
            <div :class="{ 'active show': tab === 'tab-2' }" x-show="tab === 'tab-2'" class="" style="display: none;">
                <div class="span-12 tab-content">
              <div class="span-12 ">Please contact us for more information.</div>
            </div>
        </div>
    </div>

By default Tabs use HTMX to control the showing and hiding of tabs but this can be swapped out for say Bootstrap very easily.

HTML Layout Objects
-------------------

Similar to Component layout objects but for html elements rather than components

These live in :code:`wildcoeus.dashboards.component.layout`.

**HTML**: Simply displays the content wrapped in a div::

    HTML("Lorem ipsum dolor sit amet.")

generates::

   <div class="span-12 ">Lorem ipsum dolor sit amet.</div>

**HR**:  Displays a HR tag::

    HR()

generates::

    <hr />

**Header**: Display the header wrapped in a h tag.::

    Header(heading="Welcome", size=2)

generates::

    <h2>Welcome</h2>


Creating your own Component Layout Objects
------------------------------------------

Wildcoeus provides a few commonly used layout elements to get you started and you can easily get by with these.
If however you need to create your own Component Layout object this is very easy to do.
New component layouts should inherit from HTMLComponentLayout and provide a template_name
which is a path to a html file to render.  Lets create a new DivWithImage object.  Create a new file :code:`demo/mydashboard/layout.py`::

    from wildcoeus.dashboards.component.layout import HTMLComponentLayout

    class DivWithImage(HTMLComponentLayout):
        template_name: str = "demo/div_with_image.html"
        image_url: str = ""
        width: int = 12

Now lets create the template div_with_image.html. Create a new file :code:`demo/templates/demo/div_with_image.html`::

    <div {% if css %}class="{{ css }}"{% endif %}>
        <img src="{{ image_url }}" />
      {{ components }}
    </div>

Note that the :code:`image_url` attribute is automatically available in the template.
This is built in and allows you to include any extra attributes you may require by simply
adding them to you class.

We can now use it in our dashboard::

    from demo.mydashboard.layout

    class DemoDashboard(Dashboard):
        [...]
        DivWithImage(HTML("Lorem ipsum dolor sit amet."), image_url="https://via.placeholder.com/150")

Run your site and you should now see

.. image:: _images/custom_component_layout.png
   :alt: Custom Layout Component

If you site complains about not being able to find div_with_image.html make sure your settings include::

    TEMPLATES = [
        {
            'DIRS': [BASE_DIR / "templates",],
            [...]

