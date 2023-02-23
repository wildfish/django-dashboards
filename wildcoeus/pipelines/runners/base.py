from graphlib import TopologicalSorter
from typing import Dict, List

from wildcoeus.pipelines.reporters import PipelineReporter
from wildcoeus.pipelines.results.base import (
    PipelineExecution,
    PipelineResult,
    TaskExecution,
)


class PipelineRunner:
    """
    The base class to use when implementing a custom pipeline runner.
    """

    @classmethod
    def get_task_graph(cls, pipeline_result: PipelineResult) -> TopologicalSorter:
        """
        Returns a :code:`TopologicalSorter` (see :code:`graphlib.TopologicalSorter`)
        object representing the ordering of tasks in the pipeline.

        :param pipeline_result: The pipeline result object to build the graph from
        """
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
    def get_flat_task_list(cls, pipeline_result: PipelineResult) -> List[TaskExecution]:
        """
        Returns a list of all the tasks in an order they can be ran in order to
        conform to all runner ordering guarantees.
        :param pipeline_result: The pipeline result object to build the graph from
        """
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
        pipeline_execution: PipelineExecution,
        reporter: PipelineReporter,
    ) -> bool:
        """
        Starts the pipeline running by the runner. This will pass the parameters
        off to the :code:`run` method so the runner can handle the pipeline as it
        wishes.

        Returns :code:`True` if the pipeline was scheduled successfully, :code:`False`
        otherwise. This has no guarantee on the completion of the pipeline, just that
        it has been successfully scheduled.

        :param pipeline_execution: The pipeline execution object representing the
            pipeline to run.
        :param reporter: The reporter object to write messages to.
        """
        return self.run(
            pipeline_execution,
            reporter=reporter,
        )

    def run(
        self,
        pipeline_execution: PipelineExecution,
        reporter: PipelineReporter,
    ):  # pragma: no cover
        """
        Runs the pipeline. This should be reimplemented by each runner to schedule
        the pipeline as required.

        Returns :code:`True` if the pipeline was scheduled successfully, :code:`False`
        otherwise. This has no guarantee on the completion of the pipeline, just that
        it has been successfully scheduled.

        :param pipeline_execution: The pipeline execution object representing the
            pipeline to run.
        :param reporter: The reporter object to write messages to.
        """
        raise NotImplementedError
