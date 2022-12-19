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
        status=PipelineTaskStatus.PENDING.value,
        message="report message",
        serializable_pipeline_object=None,
        serializable_task_object=None,
    )

    reporter.report_body.assert_called_once_with(
        pipeline_task="fake",
        task_id="task-id",
        run_id="",
        status="PENDING",
        message="report message",
        serializable_pipeline_object=None,
        serializable_task_object=None,
    )


def test_report_pipeline_calls_report_with_task_id_set():
    reporter = Reporter()

    reporter.report_pipeline(
        pipeline_id="pipeline-id",
        status=PipelineTaskStatus.PENDING.value,
        message="report message",
        serializable_pipeline_object=None,
        serializable_task_object=None,
    )

    reporter.report_body.assert_called_once_with(
        pipeline_id="pipeline-id",
        run_id="",
        status="PENDING",
        message="report message",
        serializable_pipeline_object=None,
        serializable_task_object=None,
    )
