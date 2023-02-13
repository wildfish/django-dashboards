Results
=======

.. warning::
   This is a work in progress! While wildcoeus supports storing task states
   in the database there is ongoing work to make this a more generalised
   storage mechanism so that results can be written to other storages (redis
   for instance).

   This information is likely to change!

When a task changes state it's new state and any status message should be
recorded in the results storage.

There are 4 types of object in the result storage:

* Pipeline Executions: This records the overall state of a pipeline being
  ran. There will only be one of these per run.
* Pipeline Results: This records the state of a single pipeline instance
  within a pipeline execution along with any pipeline object it has been
  started with. There will be one per run, per object in the
  pipeline iterator.
* Task Execution: This records the overall state of a task inside a
  pipeline result. Per run there will be on per task, per pipeline result.
* Task Result: This records the state of a task instance within a task
  execution along with any task object it was started with. Per run there
  will be one per object in a task iterator for each task.

Storage Utilities
=================

**TODO**

Some information here about using the storage rather than fetching objects
directly.