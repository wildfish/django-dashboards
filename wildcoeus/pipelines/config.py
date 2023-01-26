from django.conf import settings
from django.core.files.storage import get_storage_class
from django.utils.module_loading import import_string

from wildcoeus.pipelines.reporters.base import reporter_from_config


class Config:
    @property
    def WILDCOEUS_DEFAULT_PIPELINE_RUNNER(cls):
        runner = getattr(
            settings,
            "WILDCOEUS_PIPELINE_RUNNER",
            "wildcoeus.pipelines.runners.eager.Runner",
        )
        return import_string(runner)()

    @property
    def WILDCOEUS_DEFAULT_PIPELINE_REPORTER(cls):
        reporter = getattr(
            settings,
            "WILDCOEUS_PIPELINE_REPORTER",
            (
                "wildcoeus.pipelines.reporters.base.MultiPipelineReporter", {
                    "reporters": [
                        "wildcoeus.pipelines.reporters.logging.LoggingReporter",
                        "wildcoeus.pipelines.reporters.orm.ORMReporter",
                    ]
                }
            )
        )
        return reporter_from_config(reporter)

    @property
    def WILDCOEUS_CLEAR_LOG_DAYS(cls):
        days = getattr(
            settings,
            "WILDCOEUS_CLEAR_LOG_DAYS",
            30,
        )
        return days

    @property
    def WILDCOEUS_LOG_FILE_STORAGE(cls):
        storage = getattr(
            settings,
            "WILDCOEUS_LOG_FILE_STORAGE",
            "wildcoeus.pipelines.storage.LogFileSystemStorage",
        )
        return get_storage_class(storage)()
