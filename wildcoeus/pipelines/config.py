from django.conf import settings
from django.utils.module_loading import import_string

from wildcoeus.config import object_from_config
from wildcoeus.pipelines.runners import PipelineRunner


class Config:
    """
    Class for resolving settings related to pipelines
    """

    @property
    def WILDCOEUS_DEFAULT_PIPELINE_RUNNER(cls) -> PipelineRunner:
        """
        The pipeline runner to use by default
        """
        runner = getattr(
            settings,
            "WILDCOEUS_PIPELINE_RUNNER",
            "wildcoeus.pipelines.runners.eager.Runner",
        )
        return object_from_config(runner)

    @property
    def WILDCOEUS_DEFAULT_PIPELINE_REPORTER(cls):
        """
        The pipeline reporter to use by default
        """
        reporter = getattr(
            settings,
            "WILDCOEUS_PIPELINE_REPORTER",
            (
                "wildcoeus.pipelines.reporters.base.MultiPipelineReporter",
                {
                    "reporters": [
                        "wildcoeus.pipelines.reporters.logging.LoggingReporter",
                        "wildcoeus.pipelines.reporters.orm.ORMReporter",
                    ]
                },
            ),
        )
        return object_from_config(reporter)

    @property
    def WILDCOEUS_CLEAR_LOG_DAYS(cls):
        """
        The maximum age of logs when ``clear_tasks_and_logs`` is called if no maximum
        age is specified.
        """
        days = getattr(
            settings,
            "WILDCOEUS_CLEAR_LOG_DAYS",
            30,
        )
        return days

    @property
    def WILDCOEUS_DEFAULT_PIPELINE_STORAGE(self):
        """
        The default storage class to use when storing task results
        """
        storage = getattr(
            settings,
            "WILDCOEUS_PIPELINES_RESULTS_STORAGE",
            "wildcoeus.pipelines.results.orm.OrmPipelineResultsStorage",
        )
        return object_from_config(storage)
