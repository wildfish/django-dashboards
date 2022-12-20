from typing import Any, Optional

from django.core.files.base import ContentFile
from django.utils.timezone import now

from wildcoeus.pipelines import PipelineReporter, config
from wildcoeus.pipelines.log import logger
from wildcoeus.pipelines.storage import get_log_path


class LoggingReporter(PipelineReporter):
    def report(
        self,
        status: str,
        message: str,
        run_id: Optional[str] = None,
        pipeline_id: Optional[str] = None,
        task_id: Optional[str] = None,
        pipeline_task: Optional[str] = None,
        serializable_pipeline_object: Optional[dict[str, Any]] = None,
        serializable_task_object: Optional[dict[str, Any]] = None,
    ):
        pipeline_object_msg = None
        if serializable_pipeline_object:
            pipeline_object_msg = f"pipeline object: {serializable_pipeline_object}"

        task_object_msg = None
        if serializable_task_object:
            task_object_msg = f"task object: {serializable_task_object}"

        messages = [message, pipeline_object_msg]

        if pipeline_id:
            message = " | ".join([m for m in messages if m])
            logger.info(f"Pipeline {pipeline_id} changed to state {status}: {message}")
            self._write_log_to_file(
                run_id, f"Pipeline {pipeline_id} changed to state {status}: {message}\n"
            )
        else:
            messages.append(task_object_msg)
            message = " | ".join([m for m in messages if m])
            logger.info(
                f"Task {pipeline_task} ({task_id}) changed to state {status}: {message}"
            )
            self._write_log_to_file(
                run_id,
                f"Task {pipeline_task} ({task_id}) changed to state {status}: {message}\n",
            )

    @classmethod
    def _write_log_to_file(cls, run_id: str, content: str):
        fs = config.Config().WILDCOEUS_LOG_FILE_STORAGE
        path = get_log_path(run_id)
        d = now().strftime("%d/%b/%Y %H:%M:%S")
        content = f"[{d}]: {content}"

        if not fs.exists(path):
            fs.save(path, ContentFile(content))
        else:
            file = fs.open(path, "a+")
            file.write(content)
            fs.save(path, file)
            file.close()
