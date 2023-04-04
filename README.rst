=================
Django Dashboards
=================

Tools to help you build data dashboards in Django.

https://github.com/wildfish/django-dashboards

.. image:: https://github.com/wildfish/django-dashboards/actions/workflows/build.yml/badge.svg
    :target: https://github.com/wildfish/django-dashboards

.. image:: https://coveralls.io/repos/wildfish/django-dashboards/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/wildfish/django-dashboards?branch=main

Features
========

* Dashboard view generation with components including stats, tables, charts and more.
* HTMX driven dashboards and templates for a modern MPA interface.

Supports Django 3.2 to 4.1, on Python 3.9+.

See the `full documentation <https://django-dashboards.readthedocs.io>`_ for details
of how django-dashboards works.

.. inclusion-quickstart-do-not-remove

Quickstart
==========

This is a quickstart guide for creating a simple dashboard.

Project Setup
-------------

We recommend using a virtual environment such as `pyenv <https://github.com/pyenv/pyenv>`_ to manage your
dependencies and Python versions. From this point we assume you have a environment setup, activated & pip installed.

Create a new Django project::

    # Create the project directory
    mkdir demo
    cd demo

    # Install
    pip install django-dashboards

    # Set up a new project
    django-admin startproject demo .
    cd demo
    django-admin startapp mydashboard
    cd ..

    # Sync the database
    python manage.py migrate

Dashboards
----------
First you need to setup a dashboard definition.  Create a new file :code:`demo/mydashboard/dashboards.py`::

    from dashboards.dashboard import Dashboard
    from dashboards.component import Text, Chart
    from dashboards.registry import registry
    from demo.mydashboard.data import DashboardData

    class DemoDashboard(Dashboard):
        text_example = Text(value="Lorem ipsum dolor sit amet, consectetur adipiscing elit....")
        chart_example = Chart(defer=DashboardData.fetch_bar_chart_data)

        class Meta:
            name = "Demo Dashboard"

    registry.register(DemoDashboard)

Remember to register your dashboard class in order for it to work with the auto urls.

Data
----
Data for the dashboard component can be inline (text_example) or come from a callable (chart_example).
In the example above the data for chart_example is returned from fetch_bar_chart_data.  We set this up now.
Create a new file :code:`demo/mydashboard/data.py`::

    import json

    class DashboardData:
        @staticmethod
        def fetch_bar_chart_data(**kwargs) -> str:
            data = {"giraffes": 20, "orangutans": 14, "monkeys": 23}

            return json.dumps(dict(
                data=[
                    dict(
                        x=list(data.keys()),
                        y=list(data.values()),
                        type="bar",
                    )
                ]
            )

This returns a json object with values for x, y, and type.  This is interporated by the component and rendered as a bar chart.

Config
------
In order to get the auto urls to register we need to update :code:`demo/mydashboard/apps.py`::

    from django.apps import AppConfig

    class MydashboardConfig(AppConfig):
        default_auto_field = 'django.db.models.BigAutoField'
        name = 'demo.mydashboard'

        def ready(self):
            # for registry
            import demo.mydashboard.dashboards  # type: ignore # noqa


URLs
----
Next we need to wire up the dashboard urls.  In :code:`demo/urls.py`::

    from django.contrib import admin
    from django.urls import include, path

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('dashboards/', include('dashboards.urls')),
    ]

Settings
--------
Finally add :code:`dashboards` and your new app :code:`demo.mydashboard` to INSTALLED_APPS in :code:`demo/settings.py`::

    INSTALLED_APPS = [
        ...
        "dashboards",
        "demo.mydashboard",
    ]

And we're done.

Viewing the Dashboard
---------------------
Start the Django server from the command line.::

    python manage.py runserver

The dashboard urls are automatically generated based on the app name and dashboard meta name.
For this demo the url will be :code:`http://127.0.0.1:8000/dashboards/mydashboard/demodashboard/`

.. image:: _images/quickstart_dashboard.png
   :alt: Demo Dashboard

.. inclusion-quickstart-end-do-not-remove
