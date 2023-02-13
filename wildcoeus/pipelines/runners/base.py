from graphlib import TopologicalSorter
from typing import Dict, List

from wildcoeus.pipelines.reporters import PipelineReporter
from wildcoeus.pipelines.results.base import (
    BasePipelineExecution,
    BasePipelineResult,
    BaseTaskExecution,
)


class PipelineRunner:
    @classmethod
    def get_task_graph(cls, pipeline_result: BasePipelineResult) -> TopologicalSorter:
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

        return TopologicalSorter(task_graph)

    @classmethod
    def get_flat_task_list(
        cls, pipeline_result: BasePipelineResult
    ) -> List[BaseTaskExecution]:
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

        task_order = tuple(cls.get_task_graph(pipeline_result).static_order())
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
