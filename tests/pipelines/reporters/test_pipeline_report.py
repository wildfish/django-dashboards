from unittest.mock import Mock

from wildcoeus.pipelines import PipelineReporter, PipelineTaskStatus


class Reporter(PipelineReporter):
    def __init__(self):
        self.report_body = Mock()

    def report(self, *args, **kwargs):
        self.report_body(*args, **kwargs)


def test_report_task_calls_report_with_task_id_set():
    reporter = Reporter()

    reporter.report_task(
        pipeline_task="fake",
        task_id="task-id",
        status=PipelineTaskStatus.PENDING,
        message="report message",
        object_lookup=None,
    )

    reporter.report_body.assert_called_once_with(
        None,
        "fake",
        "task-id",
        PipelineTaskStatus.PENDING,
        "report message",
        None,
    )


def test_report_pipeline_calls_report_with_task_id_set():
    reporter = Reporter()

    reporter.report_pipeline(
        pipeline_id="pipeline-id",
        status=PipelineTaskStatus.PENDING,
        message="report message",
        object_lookup=None,
    )

    reporter.report_body.assert_called_once_with(
        "pipeline-id",
        None,
        None,
        PipelineTaskStatus.PENDING,
        "report message",
        None,
    )
