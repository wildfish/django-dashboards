Pipelines
=========

Pipelines are used to define how your offline tasks should be ran.
Each can be configured with a set of tasks to run, the order in
which they should run as well as an expected configuration and
input data format.

To create a pipeline, you must create a :code:`piplines.py` file
in your django app containing a class that extends the base
:code:`Pipeline` class::

    from wildcoeus.pielines.base import Pipeline


    class CustomPipeline(Pipeline):
        ...

Tasks can then be added by, by default they will be ran in the order
they are defined in the pipeline::

    from wildcoeus.pielines.base import Pipeline


    class CustomPipeline(Pipeline):
        # this will be ran first
        first = SomeTask()

        # this will be ran second
        second = SomeOtherTask()

Meta
----

Each pipeline may supply a custom :code:`Meta` class. This is
combined with the :code:`Meta` classes from each of the pipelines
base classes to create a merged metaclass accessible from the
:code:`_meta` property of the pipeline. To do this add create
a class called :code:`Meta` as a child of the pipeline object::

    from django.utils.translation import gettext_lazy as _
    from wildcoeus.pielines.base import Pipeline


    class CustomPipeline(Pipeline):
        # this will be ran first
        first = SomeTask()

        # this will be ran second
        second = SomeOtherTask()

        class Meta:
            name = _("Custom Pipeline")
            verbose_name = _("My Detailed Custom Pipeline")

The base pipeline meta class contains the following properties:

* :code:`abstract` (:code:`bool`): When a pipeline is flagged as abstract
  it is excluded from the internal pipeline registry and so will not
  appear in any menus and will not be runnable. If not specified, this will
  be :code:`False` even if a parent class is flagged as abstract.
* :code:`name` (:code:`str`): A short name for the pipeline to appear in
  menus etc. If not set the name of the pipeline class is used.
* :code:`verbose_name` (:code:`str`): A long name for the pipeline to appear in
  as titles etc. If not set the :code:`name` is used.
* :code:`app_label` (:code:`str`): The name of the application the pipeline is
  part of, used when looking up pipelines from the registry. In not set the
  :code:`app_label` is discovered from the django app registry.

Iterators
---------

A pipeline can be have a `get_iterator` method. This will cause the pipeline to
be ran for each element in the returned value with the value being passed into
each task::

    class CustomPipeline(Pipeline):
        ...

        def get_iterator(self):
            return [1, 2, 3]

In this example the pipeline will be ran 3 times with the values 1, 2, and 3.

Model Pipelines
===============

Model pipelines allow you to run a pipeline for all or a subset of entries
for a specific model. Rather than extending the :code:`Pipeline` object, the
:code:`ModelPipeline` should be used.

There are 2 options for defining the queryset, either:

* setting the model in the pipeline meta class, this will run the pipeline for
  each object in the database::

      from wildcoeus.pielines.base import ModelPipeline


      class CustomPipeline(ModelPipeline):
          ...

          class Meta:
              model = CustomModel

* defining a :code:`get_queryset` on the pipeline. Currently this can only be
  used to define objects that can be passed into the pipeline, more complex
  queries are not supported eg aggregates and annotations::

      from wildcoeus.pielines.base import ModelPipeline


      class CustomPipeline(ModelPipeline):
          ...

          def get_queryset(self):
             return CustomModel.objects.all()

Ordering
--------

By default, tasks are ran in the order they are defined in the pipeline with the
first needing to be completed before the second is started and so on. This can
be overridden however by supplying an :code:`ordering` property. This is a
dictionary where each key is the name of a task property and the values are a
list of property names the task is dependant on.

.. note::
   If an :code:`ordering` property is defined, anything not present in the dictionary
   is assumes to have no dependencies and can be started at any point.

In the following example there are 4 tasks :code:`a`, :code:`b`, :code:`c` and :code:`d`.
An ordering property has been provided but ordering for :code:`a` and :code:`d` is not
defined so they can be ran at any point at the runners discretion. Task :code:`b` must
wait for :code:`a` to have finished and task :code:`c` must wait for task :code:`b` to
have finished but no tasks need to wait for :code:`d` to have finished as :code:`d` is not
listed as a dependency of any task::

    from wildcoeus.pipelines.base import Pipeline

    ...

    class CustomPipeline(Pipeline):
        a = A()
        b = B()
        c = C()
        d = D()

        ordering = {
            "b": ["a"],
            "c": ["b"],
        }
