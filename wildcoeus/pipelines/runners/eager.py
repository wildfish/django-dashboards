from typing import Any, Dict, Iterable, List, Optional

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
        tasks: List[Task],
        ran_pipeline_tasks: List[str],
    ) -> Iterable[Task]:
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
        pipeline_id: str,
        run_id: str,
        tasks: List[Task],
        input_data: Dict[str, Any],
        reporter: PipelineReporter,
        pipeline_object: Optional[Any] = None,
    ) -> bool:

        pipeline = pipeline_registry.get_pipeline_class(pipeline_id)
        serializable_pipeline_object = pipeline.get_serializable_pipeline_object(
            obj=pipeline_object
        )

        self._report_pipeline_running(
            pipeline_id=pipeline_id,
            run_id=run_id,
            reporter=reporter,
            serializable_pipeline_object=serializable_pipeline_object,
        )

        ran_pipeline_tasks: List[str] = []

        for task in self._get_next_task(tasks, ran_pipeline_tasks):
            iterator = task.get_iterator()
            if not iterator:
                iterator = [None]

            print(iterator)
            for i in iterator:
                print("here")
                res = task.start(
                    pipeline_id=pipeline_id,
                    run_id=run_id,
                    input_data=input_data,
                    reporter=reporter,
                    serializable_pipeline_object=serializable_pipeline_object,
                    serializable_task_object=task.get_serializable_task_object(i),
                )
            print(res)
            if res:
                ran_pipeline_tasks.append(task.pipeline_task)
            else:
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

                return False

        self._report_pipeline_done(
            pipeline_id=pipeline_id,
            run_id=run_id,
            reporter=reporter,
            serializable_pipeline_object=serializable_pipeline_object,
        )

        return True
