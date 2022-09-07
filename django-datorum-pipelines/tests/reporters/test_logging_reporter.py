from unittest.mock import Mock, patch

from datorum_pipelines import PipelineTaskStatus
from datorum_pipelines.reporters.logging import LoggingReporter


def test_report_task_writes_the_message_to_info():
    mock_logger = Mock()

    with patch(
        "datorum_pipelines.reporters.logging.get_logger", Mock(return_value=mock_logger)
    ):
        LoggingReporter().report_task("task_id", PipelineTaskStatus.DONE, "Done")

        mock_logger.info.assert_called_once_with(
            "Task task_id changed to state DONE: Done"
        )


def test_report_pipeline_writes_the_message_to_info():
    mock_logger = Mock()

    with patch(
        "datorum_pipelines.reporters.logging.get_logger", Mock(return_value=mock_logger)
    ):
        LoggingReporter().report_pipeline(
            "pipeline_id", PipelineTaskStatus.DONE, "Done"
        )

        mock_logger.info.assert_called_once_with(
            "Pipeline pipeline_id changed to state DONE: Done"
        )
