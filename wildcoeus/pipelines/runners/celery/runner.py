import itertools
from typing import Any, Dict, List, Optional

from celery import chain

from wildcoeus.pipelines import PipelineReporter, PipelineTaskStatus
from wildcoeus.pipelines.log import logger
from wildcoeus.pipelines.registry import pipeline_registry
from wildcoeus.pipelines.runners import PipelineRunner
from wildcoeus.pipelines.tasks import Task

from .tasks import run_pipeline_report, run_task, run_task_report


class Runner(PipelineRunner):
    @staticmethod
    def _task_to_celery_tasks(
        task: Task,
        pipeline_id: str,
        run_id: str,
        input_data: Dict[str, Any],
        serializable_pipeline_object: Optional[dict[str, Any]],
    ):
        """
        Start a task async. Task reports will be inline however, we add a link error incase
        anything occurs above task.
        """

        iterator = task.get_iterator()
        if not iterator:
            iterator = [None]

        tasks = []
        for i in iterator:
            celery_task = run_task.si(
                task_id=task.task_id,
                run_id=run_id,
                pipeline_id=pipeline_id,
                input_data=input_data,
                serializable_pipeline_object=serializable_pipeline_object,
                serializable_task_object=task.get_serializable_task_object(i),
            )
            celery_task.link_error(
                run_task_report.si(
                    task_id=task.task_id,
                    pipeline_task=task.pipeline_task,
                    run_id=run_id,
                    status=PipelineTaskStatus.RUNTIME_ERROR.value,
                    message="Task Error",
                    serializable_pipeline_object=serializable_pipeline_object,
                    serializable_task_object=task.get_serializable_task_object(i),
                )
            )

            # set to queue if defined in config
            celery_task.set(queue=getattr(task.cleaned_config, "celery_queue", None))

            tasks.append(celery_task)

        return tasks

    def start_runner(
        self,
        pipeline_id: str,
        run_id: str,
        tasks: List[Task],
        input_data: Dict[str, Any],
        reporter: PipelineReporter,
        pipeline_object: Optional[Any] = None,
    ) -> bool:
        ordered_tasks = self._get_task_graph(tasks=tasks)

        pipeline = pipeline_registry.get_pipeline_class(pipeline_id)
        serializable_pipeline_object = pipeline.get_serializable_pipeline_object(
            obj=pipeline_object
        )

        c = chain(
            # Report starting
            run_pipeline_report.si(
                pipeline_id=pipeline_id,
                run_id=run_id,
                status=PipelineTaskStatus.RUNNING.value,
                message="Running",
                serializable_pipeline_object=serializable_pipeline_object,
            ),
            # Run tasks in graph order
            *list(
                itertools.chain(
                    *map(
                        lambda t: self._task_to_celery_tasks(
                            task=t,
                            pipeline_id=pipeline_id,
                            run_id=run_id,
                            input_data=input_data,
                            serializable_pipeline_object=serializable_pipeline_object,
                        ),
                        ordered_tasks,
                    )
                )
            ),
            # Report Done
            run_pipeline_report.si(
                pipeline_id=pipeline_id,
                run_id=run_id,
                status=PipelineTaskStatus.DONE.value,
                message="Done",
                serializable_pipeline_object=serializable_pipeline_object,
            ),
        )
        c.link_error(
            # Report pipeline error
            run_pipeline_report.si(
                pipeline_id=pipeline_id,
                run_id=run_id,
                status=PipelineTaskStatus.RUNTIME_ERROR.value,
                message="Pipeline Error - remaining tasks cancelled",
                serializable_pipeline_object=serializable_pipeline_object,
            )
        )

        return c()
