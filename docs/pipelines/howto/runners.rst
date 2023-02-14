Runners
=======

In wildcoeus the pipelines and runners are kept separate meaning how the tasks
are ran can me modified based on on your requirements.

To specify a runner to use for pipelines set :code:`WILDCOEUS_PIPELINE_RUNNER`.
By default this is set to the eager runner (:code:`wildcoeus.pipelines.runners.eager.Runner`).

Currently wildcoueus ships with the following runners:

* Eager (:code:`wildcoeus.pipelines.runners.eager.Runner`): This will run all
  tasks to run in sequence, locally.
* Celery (:code:`wildcoeus.pipelines.runners.celery.runner.Runner`): This will
  create a celery canvas that will run the pipeline on celery workers.

Ordering
--------

All runners must follow the following rules:

* A task cannot run without all of its parents being completed
* A task without a parent can be ran at any point
* If a pipeline has an iterator the runner must run all pipelines independently.
  If one errors, the rest should be ran to completion.
* If a task has an iterator the runner must run all instances of the task before
  running any child tasks. If any tasks in the iterator fail, the remaining
  tasks should be cancelled. This cancellation isn't guaranteed however (for
  instance tasks already running on a celery worker may complete) but all child
  tasks are guaranteed to be cancelled.

It is down to the runner to decide how to interpret the task graph and schedule
each task. It is allowed to do this in any way as long as these four rules are
followed.

Eager Runner
------------

The eager runner runs all tasks in series on your local machine. This is useful
when developing a pipeline but is not intended for use in production.

Celery Runner
-------------

The celery runner is designed to build a celery canvas which is then scheduled
on a group of celery workers. Each pipeline in an iterator will generate it's
own canvas building a chain of tasks, each of which will be chord if an
iterator defined.

It is left to the reader to design and implement their own celery deployment.
`Here <https://docs.celeryq.dev/en/stable/getting-started/introduction.html>`_
is the celery documentation with some useful information for implementing with
django `here <https://docs.celeryq.dev/en/stable/django/index.html?highlight=django>`_.

Custom Runners
--------------

To build a custom runner a :code:`start_runner` method must be defined taking 2
parameters:

* :code:`pipeline_execution` (a :code:`PipelineExecution` object)
* :code:`reporter` (a :code:`PipelineReporter` object)

This should build a schedule that will run each task and catch any errors and record
them in the :doc:`results storage <./results.rst>`. To help with this the base
:code:`PipelineRunner` class provides 2 methods:

* :code:`get_task_graph`: Which creates a :code:`TopologicalSorter` object from
  the task dependencies (see the `graphlib <https://docs.python.org/3/library/graphlib.html>`_
  documentation).
* :code:`get_flat_task_list`: Which provides a list of :code:`TaskExecution` objects that
  can be ran in order to abide by the rules set out above.

If the pipelines are successfully scheduled the method should return :code:`True`
otherwise return :code:`False` or raise an :code:`Exception`.
