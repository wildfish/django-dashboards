from graphlib import TopologicalSorter
from typing import Dict, List

from wildcoeus.pipelines.reporters import PipelineReporter
from wildcoeus.pipelines.results.base import (
    BasePipelineExecution,
    BasePipelineResult,
    BaseTaskExecution,
)


class PipelineRunner:
    @staticmethod
    def _get_task_graph(pipeline_result: BasePipelineResult) -> List[BaseTaskExecution]:
        task_graph: Dict[str, List[str]] = {}

        pipeline = pipeline_result.get_pipeline()

        if pipeline.ordering is None:
            prev = ""
            for task in (pipeline.tasks or {}).keys():
                task_graph[task] = [prev] if prev else []
                prev = task
        else:
            task_graph = {**pipeline.ordering}
            for task in (pipeline.tasks or {}).keys():
                task_graph.setdefault(task, [])

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
