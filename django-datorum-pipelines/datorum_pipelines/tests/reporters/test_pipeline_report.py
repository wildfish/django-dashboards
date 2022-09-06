from unittest.mock import Mock

from datorum_pipelines import BasePipelineReporter, PipelineTaskStatus


class Reporter(BasePipelineReporter):
    def __init__(self):
        self.report_body = Mock()

    def report(self, *args, **kwargs):
        self.report_body(*args, **kwargs)


def test_report_task_calls_report_with_task_id_set():
    reporter = Reporter()

    reporter.report_task("task-id", PipelineTaskStatus.PENDING, "report message")

    reporter.report_body.assert_called_once_with(
        None, "task-id", PipelineTaskStatus.PENDING, "report message"
    )


def test_report_pipeline_calls_report_with_task_id_set():
    reporter = Reporter()

    reporter.report_pipeline(
        "pipeline-id", PipelineTaskStatus.PENDING, "report message"
    )

    reporter.report_body.assert_called_once_with(
        "pipeline-id", None, PipelineTaskStatus.PENDING, "report message"
    )
