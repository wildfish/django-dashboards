import uuid
from typing import Any, Dict, List

from celery import chain

from datorum_pipelines import PipelineTaskStatus
from datorum_pipelines.reporters import BasePipelineReporter
from datorum_pipelines.runners import BasePipelineRunner
from datorum_pipelines.tasks import BaseTask

from .tasks import run_pipeline_report, run_task, run_task_report


class Runner(BasePipelineRunner):
    @staticmethod
    def _task_to_celery_task(task, pipeline_id, input_data):
        """
        Start a task async. Task reports will be inline however, we add a link error incase
        anything occurs above task.
        """
        celery_task = run_task.si(
            task_id=task.task_id,
            run_id=str(uuid.uuid4()),
            pipeline_id=pipeline_id,
            input_data=input_data,
        )
        celery_task.link_error(
            run_task_report.si(
                task_id=task.task_id,
                pipeline_id=pipeline_id,
                status=PipelineTaskStatus.RUNTIME_ERROR,
                message="Task Error",
            )
        )
        return celery_task

    def start(
        self,
        pipeline_id: str,
        tasks: List[BaseTask],
        input_data: Dict[str, Any],
        **kwargs,
    ) -> bool:

        ordered_tasks = self._get_task_graph(tasks=tasks)

        c = chain(
            # Report starting
            run_pipeline_report.si(
                pipeline_id=pipeline_id,
                status=PipelineTaskStatus.RUNNING,
                message="Running",
            ),
            # Run tasks in graph order
            *map(
                lambda t: self._task_to_celery_task(
                    task=t, pipeline_id=pipeline_id, input_data=input_data
                ),
                ordered_tasks,
            ),
            # Report Done
            run_pipeline_report.si(
                pipeline_id=pipeline_id, status=PipelineTaskStatus.DONE, message="Done"
            ),
        )
        c.link_error(
            # Report pipeline error
            run_pipeline_report.si(
                pipeline_id=pipeline_id,
                status=PipelineTaskStatus.RUNTIME_ERROR,
                message="Pipeline Error - remaining tasks cancelled",
            )
        )

        return c
