====
Demo
====

We also have a demo for those who'd just prefer to have a dig around some examples, you can get it running via
docker with::

    mkdir django-dashboards-demo
    cd django-dashboards-demo

    git clone git@github.com:wildfish/django-dashboards.git

    cd django-dashboards/demos/dashboard

    cp dev-docker-compose.yml.default dev-docker-compose.yml

    docker-compose -f dev-docker-compose.yml up --build


Now visit `http://127.0.0.1:8000 <http://127.0.0.1:8000>`_

.. note::
   If you want to see the SSE demo in action in another terminal start:

   ``docker-compose -f dev-docker-compose.yml run django python manage.py send_sse``


.. image:: _images/demo.gif
   :alt: Demo