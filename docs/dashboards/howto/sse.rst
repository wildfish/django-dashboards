==================
Server sent events
==================

While we don't have any direct support for websockets or SSE components out the box.
It is possible to build your own SSE component leveraging a few tools.

You can find a couple of examples of this in our demos (TODO add links).

+++++++++++++++++++++++++
Using SSE in your project
+++++++++++++++++++++++++

To use SSE you need django_eventstream and an event service such as pushpin.

Install django_eventstream
++++++++++++++++++++++++++

::

    pip install django_eventstream

Add the following to your settings file:

::

    INSTALLED_APPS = [
        ...
        'django_eventstream',
    ]

    MIDDLEWARE = [
        'django_grip.GripMiddleware',
         ...
    ]

    GRIP_URL = 'http://localhost:5561'
    EVENTSTREAM_ALLOW_ORIGIN = "http://127.0.0.1:8000"

Add url pattern for SSE channels

::

        dashboard_channels = []  # per dashboard, per component etc
        urlpatterns += [path('events/', include(django_eventstream.urls), {"channels": dashboard_channels})]


Additional notes:

* Refer to django_eventstream regarding authentication
* This is posting all events to test, you'd want to consider spreading events to different
  channels for dashboards/components e.g. https://github.com/fanout/django-eventstream#routes-and-channel-selection

Run pushpin
+++++++++++

For our demo we use pushpin to aid with event distribution. The easiest way to start pushpin locally is to add it to a docker compose i.e.

::

  pushpin:
    image: fanout/pushpin
    environment:
      target: '127.0.0.1:8000'
    volumes:
      - "./pushpin.conf:/etc/pushpin/:rw"
    network_mode: host



where pushpin.conf/ is a folder containing a routes file with the following:

::

    * 127.0.0.1:8000,over_http


Additional notes:

* You will also need to deploy a pushpin instance or use Fanout Cloud (see below).


Add your SSE components
+++++++++++++++++++++++

Once eventstream and pushpin are setup iou can create a component that accepts SSE quite easily.
In our demo we the following which uses a new template and a pushpin_url for the Stat and Chart components:

::

    from wildcoeus.dashboards.component import Chart, Stat
    from dataclasses import dataclass
    from typing import Optional

    @dataclass
    class SSEStat(Stat):
        template: str = "wildcoeus/dashboards/components/sse_stat.html"
        poll_rate: Optional[int] = 10

        @staticmethod
        def pushpin_url():
            """
            Assuming docker pushpin is running, in real world this would be proxied to application.
            """
            return "http://localhost:7999/events/"


    @dataclass
    class SSEChart(Chart):
        template: str = "wildcoeus/dashboards/components/sse_chart.html"
        poll_rate: Optional[int] = None

        @staticmethod
        def pushpin_url():
            """
            Assuming docker pushpin is running, in real world this would be proxied to application.
            """
            return "http://localhost:7999/events/"


    ...

    class DemoDashboard(Dashboard):
        sse_stat = SSEStat()
        ...


At a template level, taking SSEStat as an example, we can then leverage HTMX to connect to pushpin

::

    <div hx-ext="sse" sse-connect="{{ component.pushpin_url }}" sse-swap="{{ component.key }}">
      Contents of this box will be updated in real time
      with every SSE received.
    </div>


In order for events to be send you could either have a cron job, management command, celery task or one even
of our pipelines. For example in our demo, we render the stat and resend the stat as follows:

::

    value = randint(1, 100)
    sse_stat = Stat(
        value={"text": f"{value}%", "sub_text": "Via SSE"}, key="sse_stat"
    )
    rendered_stat = render_to_string(
        sse_stat.template,
        {
            "component": sse_stat,
            "rendered_value": sse_stat.get_value(),
        },
    )

    parsed_stat = strip_spaces_between_tags(rendered_stat.strip())

    # Here we return a actual rendered stat component, but this could be simply a value JSON also
    send_event("test", "sse_stat", parsed_stat, json_encode=False)

This will send a stat via an event to the ``sse_stat`` component.