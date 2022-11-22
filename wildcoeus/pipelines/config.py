from django.conf import settings
from django.utils.module_loading import import_string


class Config:
    @property
    def WILDCOEUS_DEFAULT_PIPELINE_RUNNER(cls):
        runner = getattr(
            settings,
            "WILDCOEUS_PIPELINE_RUNNER",
            "wildcoeus.pipelines.runners.celery.Runner",
        )
        return import_string(runner)()

    @property
    def WILDCOEUS_DEFAULT_PIPELINE_REPORTER(cls):
        reporter = getattr(
            settings,
            "WILDCOEUS_PIPELINE_REPORTER",
            "wildcoeus.pipelines.reporters.logging.LoggingReporter",
        )
        return import_string(reporter)()
