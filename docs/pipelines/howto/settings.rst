Settings
========

WILDCOEUS_DEFAULT_PIPELINE_RUNNER
---------------------------------

A python path to the runner to use.

**default** :code:`wildcoeus.pipelines.runners.eager.Runner`

WILDCOEUS_DEFAULT_PIPELINE_REPORTER
-----------------------------------

Either a python path to the reporter to use or a 2-tuple where the
first element is the python path to the reporter and the second is
a dictionary of keyword arguments to pass to the reporter on
construction.

**default**::

    (
        "wildcoeus.pipelines.reporters.base.MultiPipelineReporter",
        {
            "reporters": [
                "wildcoeus.pipelines.reporters.logging.LoggingReporter",
                "wildcoeus.pipelines.reporters.orm.ORMReporter",
            ]
        },
    )

WILDCOEUS_CLEAR_LOG_DAYS
------------------------

The default number of days to use when clearing the logs.

**default** :code:`30`
