from graphlib import TopologicalSorter
from typing import Any, Dict, List, Optional

from wildcoeus.pipelines.reporters import PipelineReporter
from wildcoeus.pipelines.results.base import BaseTaskResult, BasePipelineResult, BasePipelineExecution, \
    BaseTaskExecution
from wildcoeus.pipelines.status import PipelineTaskStatus
from wildcoeus.pipelines.tasks import Task


class PipelineRunner:
    @staticmethod
    def _get_task_graph(pipeline_result: BasePipelineResult) -> List[BaseTaskExecution]:
        task_graph = {}

        for task in pipeline_result.get_pipeline().tasks.values():
            task_graph[task.pipeline_task] = set(
                getattr(task.cleaned_config, "parents", [])
            )

        task_order = tuple(TopologicalSorter(task_graph).static_order())
        tasks_ordered = sorted(
            pipeline_result.get_task_executions(),
            key=lambda t: task_order.index(t.pipeline_task),
        )
        return tasks_ordered

    def start(
        self,
        pipeline_execution: BasePipelineExecution,
        reporter: PipelineReporter,
    ):
        return self.start_runner(
            pipeline_execution,
            reporter=reporter,
        )

    def start_runner(
        self,
        pipeline_execution: BasePipelineExecution,
        reporter: PipelineReporter,
    ):  # pragma: no cover
        """
        Start runner, is called by start and applies any runner specific steps.
        """
        raise NotImplementedError
