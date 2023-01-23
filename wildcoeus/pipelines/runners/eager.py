from typing import Iterable, List

from ..reporters import PipelineReporter
from ..results.base import BasePipelineExecution, BaseTaskExecution
from ..status import PipelineTaskStatus
from .base import PipelineRunner


class Runner(PipelineRunner):
    def _task_can_be_ran(
        self,
        task_execution: BaseTaskExecution,
        ran_pipeline_tasks: List[str],
    ):
        task = task_execution.get_task()
        not_all_parents_ran = any(
            map(
                lambda parent: parent not in ran_pipeline_tasks,
                getattr(task.cleaned_config, "parents", []),
            )
        )

        return task.pipeline_task not in ran_pipeline_tasks and not not_all_parents_ran

    def _get_next_task(
        self,
        tasks: Iterable[BaseTaskExecution],
        ran_pipeline_tasks: List[str],
    ) -> Iterable[BaseTaskExecution]:
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
        pipeline_execution: BasePipelineExecution,
        reporter: PipelineReporter,
    ) -> bool:
        for pipeline_result in pipeline_execution.get_pipeline_results():
            ran_pipeline_tasks: List[str] = []

            failed = False
            for task_execution in self._get_next_task(
                pipeline_result.get_task_executions(), ran_pipeline_tasks
            ):
                task = task_execution.get_task()
                task_results = task_execution.get_task_results()

                for task_result in task_results:
                    try:
                        if not failed:
                            task.start(
                                task_result,
                                reporter=reporter,
                            )
                        else:
                            task_result.report_status_change(
                                reporter,
                                PipelineTaskStatus.CANCELLED,
                                message="There was an error running a different task",
                            )
                    except Exception:
                        # if a task fails record all others have been canceled
                        failed = True

                ran_pipeline_tasks.append(task.pipeline_task)

            pipeline_result.report_status_change(
                reporter, PipelineTaskStatus.DONE, propagate=False
            )

        pipeline_execution.report_status_change(reporter, PipelineTaskStatus.DONE)

        return True
