from graphlib import TopologicalSorter
from typing import Any, Dict, List

from .. import BasePipelineReporter
from ..status import PipelineTaskStatus
from ..tasks import BaseTask


class BasePipelineRunner:
    @staticmethod
    def _report_task_cancelled(task, reporter):
        reporter.report_task(
            pipeline_task=task.pipeline_task,
            task_id=task.task_id,
            status=PipelineTaskStatus.CANCELLED,
            message="There was an error running a different task",
        )

    @staticmethod
    def _report_pipeline_running(pipeline_id, reporter):
        reporter.report_pipeline(
            pipeline_id=pipeline_id,
            status=PipelineTaskStatus.RUNNING,
            message="Running",
        )

    @staticmethod
    def _report_pipeline_done(pipeline_id, reporter):
        reporter.report_pipeline(
            pipeline_id=pipeline_id, status=PipelineTaskStatus.DONE, message="Done"
        )

    @staticmethod
    def _report_pipeline_error(pipeline_id, reporter):
        reporter.report_pipeline(
            pipeline_id=pipeline_id,
            status=PipelineTaskStatus.RUNTIME_ERROR,
            message="Error",
        )

    @staticmethod
    def _get_task_graph(tasks: List[BaseTask]) -> List[BaseTask]:
        task_graph = {}

        for task in tasks:
            task_graph[task.pipeline_task] = set(
                getattr(task.cleaned_config, "parents", [])
            )

        task_order = tuple(TopologicalSorter(task_graph).static_order())
        tasks_ordered = sorted(tasks, key=lambda t: task_order.index(t.pipeline_task))
        return tasks_ordered

    def start(
        self,
        pipeline_id: str,
        run_id: str,
        tasks: List[BaseTask],
        input_data: Dict[str, Any],
        reporter: BasePipelineReporter,
    ) -> bool:  # pragma: no cover
        raise NotImplementedError
