Reporters
=========

Reporters allow for messages from the tasks being ran to be written so that
they can be retrieved at a later date.

The default reporter used can be configured by changing the
:code:`WILDCOEUS_PIPELINE_REPORTER`. By default this is setup to use the
standard python logging and ORM logging.

.. note::
   For the pipeline status views to work correctly the ORM logging must be
   used.

Custom Reporters
----------------

If you wish to write a custom reporter you must extend the :code:`PipelineReporter`
from :code:`wildcoeus.pielines.reporters.base`. This should implement a :code:`report`
method which takes 3 parameters:

* :code:`context_object`: One of the pipeline result objects
* :code:`status`: The new :code:`PipelineStatus` of the the object to report on
* :code:`message`: The message to record

For example, the following would print to the console output::

    from wildcoeus.pielines.reporters.base import PipelineReporter

    class PrintReporter(PipelineReporter):
        def report(self, context_object, status, message):
            print(f"{context_object}: New Status {status} - {message}")

If your reporter requires any arguments on construction they must be acceptable as
keyword arguments and configurable from the django settings file.

Multiple Reporters
------------------

To enable multiple reporters to be used at the same time, wildcoeus ships
with :code:`MultiPipelineReporter` from :code:`wildcoeus.pielines.reporters.base`.
This loads all the reporters provided in the :code:`reporters` keyword argument
and will forward any report calls onto each.

See :doc:`here <./settings>` for more information on configuring reporters.
