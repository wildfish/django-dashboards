Results
=======

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

Rather than interacting with the storage directly you should use the set
of utility methods defined in :code:`wildcoeus.pipelines.results.helpers`.
This module provides a set of methods for creating and fetching result
objects from the storage and will work for all storage classes provided
they follow the defined interface.

Custom Storage Class
====================

To define you own custom storage class you must extend the base storage
class (:code:`wildcoeus.pipelines.results.base.PipelineStorage`) and each
object returned will need to extend the relevant storage object (
:code:`wildcoeus.pipelines.results.base.PipelineExecution`,
:code:`wildcoeus.pipelines.results.base.PipelineResult`,
:code:`wildcoeus.pipelines.results.base.TaskExecution` and
:code:`wildcoeus.pipelines.results.base.TaskResult`).

When accessing properties from storage objects, a :code:`get_` method
should be used. Similarly for setting values a :code:`set_` method
should be used, this allows for the maximum flexibility in how the data
is stored and retrieved.

For convenience, is a :code:`get_` method is not implemented for a given
property, it will fallback to retrieving the property by name on the
object. For example, if we try to use :code:`get_foo` to retrieve the
:code:`foo` property the object will:

1. First try to find a method called :code:`get_foo` and use that.
2. If it doesnt exist but the object has a property called :code:`foo`
   it will return a method that returns :code:`foo`.
3. If neither exist an :code:`AttributeError` will be raised as normal.

Similarly, for :code:`set_foo` methods will set :code:`foo` on the object
unless it's otherwise defined.

For an example of how to build a custom storage class see
:code:`wildcoeus.pipelines.results.orm.OrmPipelineResultsStorage`.

To override the storage class used, change the value of
:code:`WILDCOEUS_PIPELINES_RESULTS_STORAGE` in your settings file
(:code:`"wildcoeus.pipelines.results.orm.OrmPipelineResultsStorage"` by default).
This can either be a string where the value matches the python path to the
class to use or a 2-tuple where the first element matches the python path to
the class to use and the second element is a dictionary of keyword arguments
to pass to the storage class when initialised.
