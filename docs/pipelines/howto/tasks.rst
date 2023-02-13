Tasks
=====

A task is a unit of work that gets ran by a pipeline. At a minimum the task
must define a :code:`run` method, this can be used perform any python code::

    class CustomTask(Task):
        def run(self, *args, **kwargs):
            # some python code
            ...

A pydantic object can be defined that will clean the config and input data
which will clean the task config and the input data and raise errors if the
validation fails.

Iterators
---------

As with pipelines, tasks support being ran on multiple objects. To do so
define a :code:`get_iterator` method that returns an iterable. The pipeline
runner will then expand this into multiple instances of the same task passing
each object in to each.

In the following example the task will be started with values "a", "b" and "c"::

    class CustomTask(Task):
        ...

        def get_iterator(self):
            ...

Accessing Objects
-----------------

After setting up iterators for pipelines and tasks you will need to access them
when running your tasks. For this each task has :code:`pipeline_object` and
:code:`task_object` properties. The :code:`pipeline_object` will be the object
passed in from the pipelines iterator and the :code:`task_object` will be the
object passed in from the task iterator.

Config Data
-----------

The config type for a task is defined by defining a :code:`ConfigType` property
on the task class. This should extend the :code:`TaskConfig` from
:code:`wildcoeus.pipelines.tasks.base`::

    from wildcoeus.pipelines.tasks.base import TaskConfig, Task


    class CustomTask(Task):
        class ConfigType(TaskConfig):
            a: str

In this example, when adding a task to a pipeline, the task must be instantiated
with a keyword option :code:`a` which is a :code:`str`, if it is missing an error
will be raised::

    from wildcoeus.pipelines.base import Pipeline

    class CustomPipeline(Pipeline):
        # will raise an error because `a` is not supplied
        bad = CustomTask()

        # success!
        good = CustomTask(a="foo")

The config types are `pydantic <https://docs.pydantic.dev/>`_ classes and
so can do everything that can be done with other `pydantic <https://docs.pydantic.dev/>`_
objects.

.. warning::
   The :code:`ConfigType` should allow for extra fields to be supplied. This allows
   for optional parameters to be passed to the runners when ran. For example the
   celery runner allows you to pass a :code:`celery_queue` property to tasks to specify
   the queue on which the task should be scheduled.

   By default any config class extending :code:`TaskConfig` should already follow this
   behaviour.

Input Data
----------

Similar to the config type, a task can define an :code:`InputType` that extends
`pydanytics base model <https://docs.pydantic.dev/usage/models/>`_. This is used to
validate the input data provided to the pipeline. Each task should only define the values
required by the task itself.

.. warning::
   By default, pydantic models ignore any extra properties. This convention should be followed
   for :code:`InputType`s so that extra parameters aren't passed to a task causing an error.


In the following example, when :code:`CustomPipeline` is ran with :code:`{"a": "foo", "b": "bar"}`
"foo" will be passed to the first task as parameter :code:`a` and "bar" will be passed to
the second task as parameter :code:`b`::

    from pydantic import BaseModel

    from wildcoeus.pipelines.tasks.base import Task
    from wildcoeus.pipelines.base import Pipeline

    class FirstTask(Task)
        class InputType(BaseModel):
            a: str

        def run(self, a=None):
            print(a)

    class SecondTask(Task)
        class InputType(BaseModel):
            b: str

        def run(self, b=None):
            print(b)


    class CustomPipeline(Pipeline):
        first = FirstTask()
        second = SecondTask()

