import itertools
from typing import Any, Dict, List, Optional

from celery import chain, group, signature

from wildcoeus.pipelines.registry import pipeline_registry
from wildcoeus.pipelines.reporters import PipelineReporter
from wildcoeus.pipelines.runners import PipelineRunner
from wildcoeus.pipelines.status import PipelineTaskStatus
from wildcoeus.pipelines.tasks import Task

from .tasks import run_pipeline_report, run_task, run_task_report


class Runner(PipelineRunner):
    @classmethod
    def _build_celery_task(
        cls,
        task: Task,
        pipeline_id: str,
        run_id: str,
        input_data: Dict[str, Any],
        serializable_pipeline_object: Optional[dict[str, Any]],
        task_object,
    ):
        celery_task = run_task.si(
            task_id=task.task_id,
            run_id=run_id,
            pipeline_id=pipeline_id,
            input_data=input_data,
            serializable_pipeline_object=serializable_pipeline_object,
            serializable_task_object=task.get_serializable_task_object(task_object),
        )
        celery_task.link_error(
            run_task_report.si(
                task_id=task.task_id,
                pipeline_task=task.pipeline_task,
                run_id=run_id,
                status=PipelineTaskStatus.RUNTIME_ERROR.value,
                message="Task Error",
                serializable_pipeline_object=serializable_pipeline_object,
                serializable_task_object=task.get_serializable_task_object(task_object),
            )
        )

        # set to queue if defined in config
        celery_task.set(queue=getattr(task.cleaned_config, "celery_queue", None))

        return celery_task

    @classmethod
    def _expand_celery_tasks(
        cls,
        task: Task,
        pipeline_id: str,
        run_id: str,
        input_data: Dict[str, Any],
        serializable_pipeline_object: Optional[dict[str, Any]],
    ) -> signature:
        """
        Start a task async. Task reports will be inline however, we add a link error incase
        anything occurs above task.
        """

        iterator = task.get_iterator()
        if iterator is not None:
            return group(
                *(
                    cls._build_celery_task(
                        task,
                        pipeline_id,
                        run_id,
                        input_data,
                        serializable_pipeline_object,
                        i,
                    )
                    for i in iterator
                )
            )
        else:
            return cls._build_celery_task(
                task,
                pipeline_id,
                run_id,
                input_data,
                serializable_pipeline_object,
                None,
            )

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

        pipeline = pipeline_registry.get_by_id(pipeline_id)
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
            *map(
                lambda t: self._expand_celery_tasks(
                    task=t,
                    pipeline_id=pipeline_id,
                    run_id=run_id,
                    input_data=input_data,
                    serializable_pipeline_object=serializable_pipeline_object,
                ),
                ordered_tasks,
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
