============
Contributing
============

Contributions are welcome by pull request. Check the github to see what needs work.


Installing
==========

The easiest way to work on django-dashboards is to fork the project on github, then
install it to a virtualenv::

    virtualenv django-dashboards
    cd django-dashboards
    source bin/activate
    pip install -e git+git@github.com:USERNAME/django-dashboards.git#egg=django-dashboards

(replacing ``USERNAME`` with your username).

This will install the development dependencies too, and you'll find the
source ready for you to work on in the ``src`` folder of your virtualenv.


Testing
=======

Contributions will be merged more quickly if they are provided with unit tests.

Use ``pytest`` to run the python tests on your current python environment;
you can optionally specify which test to run::

    pytest tests/test_new.py
    pytest tests/test_new.py::test_specific


pytest will also generate a ``coverage`` HTML report.

Code overview
=============

TODO

Known limitations
=================

* TODO


