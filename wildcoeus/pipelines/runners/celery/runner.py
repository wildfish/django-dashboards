import uuid
from typing import Any, Dict, List, Optional

from celery import chain

from wildcoeus.pipelines import PipelineReporter, PipelineTaskStatus
from wildcoeus.pipelines.runners import PipelineRunner
from wildcoeus.pipelines.tasks import Task

from .tasks import run_pipeline_report, run_task, run_task_report


class Runner(PipelineRunner):
    @staticmethod
    def _task_to_celery_task(
        task: Task,
        pipeline_id: str,
        run_id: str,
        input_data: Dict[str, Any],
        object_lookup: Optional[dict[str, Any]],
    ):
        """
        Start a task async. Task reports will be inline however, we add a link error incase
        anything occurs above task.
        """

        print("running _task_to_celery_task")
        print(task.task_id)
        print(run_id)
        print(pipeline_id)
        print(input_data)
        print(object_lookup)
        celery_task = run_task.si(
            task_id=task.task_id,
            run_id=run_id,
            pipeline_id=pipeline_id,
            input_data=input_data,
            object_lookup=object_lookup,
            cleaned_config=task._config,
        )
        celery_task.link_error(
            run_task_report.si(
                task_id=task.task_id,
                pipeline_id=pipeline_id,
                status=PipelineTaskStatus.RUNTIME_ERROR.value,
                message="Task Error",
                object_lookup=object_lookup,
            )
        )
        # print(celery_task)
        return celery_task

    def start_runner(
        self,
        pipeline_id: str,
        run_id: str,
        tasks: List[Task],
        input_data: Dict[str, Any],
        reporter: PipelineReporter,
        obj: Optional[Any] = None,
    ) -> bool:
        print("running celery start_runner")
        ordered_tasks = self._get_task_graph(tasks=tasks)

        object_lookup = self.object_lookup(obj=obj)

        print(ordered_tasks)

        c = chain(
            # Report starting
            run_pipeline_report.si(
                pipeline_id=pipeline_id,
                status=PipelineTaskStatus.RUNNING.value,
                message="Running",
                object_lookup=object_lookup,
            ),
            # Run tasks in graph order
            *map(
                lambda t: self._task_to_celery_task(
                    task=t,
                    pipeline_id=pipeline_id,
                    run_id=run_id,
                    input_data=input_data,
                    object_lookup=object_lookup,
                ),
                ordered_tasks,
            ),
            # Report Done
            run_pipeline_report.si(
                pipeline_id=pipeline_id,
                status=PipelineTaskStatus.DONE.value,
                message="Done",
                object_lookup=object_lookup,
            ),
        )

        print(c)

        print("ending celery start_runner")
        # c.link_error(
        #     # Report pipeline error
        #     run_pipeline_report.si(
        #         pipeline_id=pipeline_id,
        #         status=PipelineTaskStatus.RUNTIME_ERROR,
        #         message="Pipeline Error - remaining tasks cancelled",
        #         object_lookup=object_lookup,
        #     )
        # )

        return c()
