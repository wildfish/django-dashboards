Management Commands
===================

:code:`pipelines`
-----------------

Starts running a pipeline. When ran you will be offered a list of registered to
pipeline to run. You optionally be able to run the pipeline using the eager runner
or the defined runner.

:code:`clear_tasks_and_logs`
----------------------------

Cleans up pipeline logs and results objects from the database if they are older
than the provided number of days. If no value is supplied the value in the
:code:`WILDCOEUS_CLEAR_LOG_DAYS` setting is used.
