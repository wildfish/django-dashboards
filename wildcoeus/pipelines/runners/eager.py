from typing import Any, Dict, Iterable, List, Optional

from ..models import PipelineResult, TaskExecution, TaskResult
from ..registry import pipeline_registry
from ..reporters import PipelineReporter
from ..tasks import Task
from .base import PipelineRunner


class Runner(PipelineRunner):
    def _task_can_be_ran(self, task: Task, ran_pipeline_tasks: List[str]):
        not_all_parents_ran = any(
            map(
                lambda parent: parent not in ran_pipeline_tasks,
                getattr(task.cleaned_config, "parents", []),
            )
        )

        return task.pipeline_task not in ran_pipeline_tasks and not not_all_parents_ran

    def _get_next_task(
        self,
        tasks: List[TaskExecution],
        ran_pipeline_tasks: List[str],
    ) -> Iterable[TaskExecution]:
        while True:
            task = next(
                (t for t in tasks if self._task_can_be_ran(t, ran_pipeline_tasks)),
                None,
            )

            if task:
                yield task
            else:
                break

    def start_runner(
        self,
        pipeline_result: PipelineResult,
        tasks: List[TaskExecution],
        reporter: PipelineReporter,
    ) -> bool:
        ran_pipeline_tasks: List[str] = []

        for task_execution in self._get_next_task(tasks, ran_pipeline_tasks):
            task = task_execution.get_task(reporter)
            iterator = task.get_iterator()
            if iterator is None:
                iterator = [None]

            task_results = [
                TaskResult(
                    execution=task_execution,
                    serializable_task_object=task.get_serializable_task_object(i),
                    config=task.cleaned_config,
                    input_data=task_execution.pipeline.input_data,
                ) for i in iterator
            ]

            try:
                for res in task_results:
                    task.start(
                        res,
                        reporter=reporter,
                        serializable_task_object=task.get_serializable_task_object(i),
                    )
            except Exception:
                # if a task fails record all others have been canceled
                for t in (
                    _t
                    for _t in tasks
                    if _t.pipeline_task != task.pipeline_task
                    and _t.pipeline_task not in ran_pipeline_tasks
                ):

                    self._report_task_cancelled(
                        task=t,
                        run_id=run_id,
                        reporter=reporter,
                        serializable_pipeline_object=serializable_pipeline_object,
                    )

                self._report_pipeline_error(
                    pipeline_id=pipeline_id,
                    run_id=run_id,
                    reporter=reporter,
                    serializable_pipeline_object=serializable_pipeline_object,
                )
                raise

            ran_pipeline_tasks.append(task.pipeline_task)

        self._report_pipeline_done(
            pipeline_id=pipeline_id,
            run_id=run_id,
            reporter=reporter,
            serializable_pipeline_object=serializable_pipeline_object,
        )

        return True
