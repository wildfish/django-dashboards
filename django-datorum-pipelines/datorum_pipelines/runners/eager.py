from typing import Any, Dict, Iterable, List

from ..reporters import BasePipelineReporter
from ..status import PipelineTaskStatus
from ..tasks import BaseTask
from .base import BasePipelineRunner


class Runner(BasePipelineRunner):
    def _task_can_be_ran(self, task: BaseTask, ran_pipeline_tasks: List[str]):
        not_all_parents_ran = any(
            map(
                lambda parent: parent not in ran_pipeline_tasks,
                getattr(task.cleaned_config, "parents", []),
            )
        )

        return task.pipeline_task not in ran_pipeline_tasks and not not_all_parents_ran

    def _get_next_task(
        self,
        tasks: List[BaseTask],
        ran_pipeline_tasks: List[str],
    ) -> Iterable[BaseTask]:
        while True:
            task = next(
                (t for t in tasks if self._task_can_be_ran(t, ran_pipeline_tasks)),
                None,
            )

            if task:
                yield task
            else:
                break

    def start(
        self,
        pipeline_id: str,
        run_id: str,
        tasks: List[BaseTask],
        input_data: Dict[str, Any],
        reporter: BasePipelineReporter,
    ) -> bool:
        reporter.report_pipeline(pipeline_id, PipelineTaskStatus.RUNNING, "Running")

        ran_pipeline_tasks: List[str] = []

        for task in self._get_next_task(tasks, ran_pipeline_tasks):
            res = task.start(pipeline_id, run_id, input_data, reporter)
            if res:
                ran_pipeline_tasks.append(task.pipeline_task)
            else:
                # if a task fails record all others have been canceled
                for t in (
                    _t
                    for _t in tasks
                    if _t.pipeline_task != task.pipeline_task
                    and _t not in ran_pipeline_tasks
                ):
                    reporter.report_task(
                        task_id=task.task_id,
                        status=PipelineTaskStatus.CANCELLED,
                        message="There was an error running a different task",
                    )
                reporter.report_pipeline(
                    pipeline_id, PipelineTaskStatus.RUNTIME_ERROR, "Error"
                )
                return False

        reporter.report_pipeline(pipeline_id, PipelineTaskStatus.DONE, "Done")
        return True
