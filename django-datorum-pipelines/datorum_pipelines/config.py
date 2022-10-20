from django.conf import settings
from django.utils.module_loading import import_string


class Config:
    @property
    def DATORUM_DEFAULT_PIPELINE_RUNNER(cls) -> str:
        runner = getattr(
            settings,
            "DATORUM_PIPELINE_RUNNER",
            "datorum_pipelines.runners.celery.Runner",
        )
        return import_string(runner)()

    @property
    def DATORUM_DEFAULT_PIPELINE_REPORTER(cls) -> str:
        reporter = getattr(
            settings,
            "DATORUM_PIPELINE_REPORTER",
            "datorum_pipelines.reporters.logging.LoggingReporter",
        )
        return import_string(reporter)()
