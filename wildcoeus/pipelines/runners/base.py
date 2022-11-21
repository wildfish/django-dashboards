import uuid
from graphlib import TopologicalSorter
from typing import Any, Dict, List, Optional, Union

from wildcoeus.pipelines import PipelineReporter
from wildcoeus.pipelines.registry import pipeline_registry
from wildcoeus.pipelines.status import PipelineTaskStatus
from wildcoeus.pipelines.tasks import Task


class PipelineRunner:
    @staticmethod
    def _report_task_cancelled(task, reporter, object_lookup=None):
        reporter.report_task(
            pipeline_task=task.pipeline_task,
            task_id=task.task_id,
            status=PipelineTaskStatus.CANCELLED,
            message="There was an error running a different task",
            object_lookup=object_lookup,
        )

    @staticmethod
    def _report_pipeline_running(pipeline_id, reporter, object_lookup=None):
        reporter.report_pipeline(
            pipeline_id=pipeline_id,
            status=PipelineTaskStatus.RUNNING,
            message="Running",
            object_lookup=object_lookup,
        )

    @staticmethod
    def _report_pipeline_done(pipeline_id, reporter, object_lookup=None):
        reporter.report_pipeline(
            pipeline_id=pipeline_id, status=PipelineTaskStatus.DONE, message="Done"
        )

    @staticmethod
    def _report_pipeline_error(pipeline_id, reporter, object_lookup=None):
        reporter.report_pipeline(
            pipeline_id=pipeline_id,
            status=PipelineTaskStatus.RUNTIME_ERROR,
            message="Error",
        )

    @staticmethod
    def _get_task_graph(tasks: List[Task]) -> List[Task]:
        task_graph = {}

        for task in tasks:
            task_graph[task.pipeline_task] = set(
                getattr(task.cleaned_config, "parents", [])
            )

        task_order = tuple(TopologicalSorter(task_graph).static_order())
        tasks_ordered = sorted(tasks, key=lambda t: task_order.index(t.pipeline_task))
        return tasks_ordered

    @staticmethod
    def object_lookup(obj):
        if not obj:
            return None

        return {
            "pk": obj.pk,
            "app_label": obj._meta.app_label,
            "model_name": obj._meta.model_name,
        }

    def start(
        self,
        pipeline_id: str,
        run_id: str,
        tasks: List[Task],
        input_data: Dict[str, Any],
        reporter: PipelineReporter,
    ):
        """
        Start a pipeline, if this is a standard Pipeline, start_runner is called as normal.

        If this is a ModelPipeline, we run against each instance in the queryset.

        TODO rate limiter on iterators.
        """
        from wildcoeus.pipelines.base import ModelPipeline

        pipeline = pipeline_registry.get_pipeline_class(pipeline_id)
        if issubclass(pipeline, ModelPipeline):
            qs = pipeline.get_queryset()
            runs = []
            for obj in qs:
                run = self.start_runner(
                    pipeline_id=pipeline_id,
                    run_id=str(uuid.uuid4()),
                    tasks=tasks,
                    input_data=input_data,
                    reporter=reporter,
                    obj=obj,
                )
                runs.append(run)
            return runs
        else:
            return self.start_runner(
                pipeline_id=pipeline_id,
                run_id=run_id,
                tasks=tasks,
                input_data=input_data,
                reporter=reporter,
            )

    def start_runner(
        self,
        pipeline_id: str,
        run_id: str,
        tasks: List[Task],
        input_data: Dict[str, Any],
        reporter: PipelineReporter,
        obj: Optional[Any] = None,
    ):  # pragma: no cover
        """
        Start runner, is called by start and applies any runner specific steps.
        """
        raise NotImplementedError
