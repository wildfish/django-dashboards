import uuid
from itertools import product
from typing import Any, Dict

from wildcoeus.pipelines.base import Pipeline
from wildcoeus.pipelines.models import (
    PipelineExecution,
    PipelineResult,
    TaskExecution,
    TaskResult,
)
from wildcoeus.pipelines.reporters import PipelineReporter
from wildcoeus.pipelines.results.base import BasePipelineResultsStorage
from wildcoeus.pipelines.runners import PipelineRunner
from wildcoeus.pipelines.status import PipelineTaskStatus


class OrmPipelineResultsStorage(BasePipelineResultsStorage):
    def build_pipeline_execution(
        self,
        pipeline: Pipeline,
        run_id: str,
        runner: PipelineRunner,
        reporter: PipelineReporter,
        input_data: Dict[str, Any],
    ):
        execution = PipelineExecution.objects.create(
            pipeline_id=pipeline.id,
            run_id=run_id,
            input_data=input_data,
        )
        reporter.report_pipeline_execution(
            execution, PipelineTaskStatus.PENDING, "Pipeline is waiting to start"
        )

        # build the pipeline results objects
        pipeline_iterator = pipeline.get_iterator()
        pipeline_objects = (
            pipeline_iterator if pipeline_iterator is not None else [None]
        )

        # cant use bulk create here as it doesnt populate the id on some databases
        # https://docs.djangoproject.com/en/4.2/ref/models/querysets/#bulk-create
        pipeline_results = [
            PipelineResult.objects.create(
                execution=execution,
                serializable_pipeline_object=pipeline.get_serializable_pipeline_object(
                    obj
                ),
                runner=f"{runner.__class__.__module__}.{runner.__class__.__name__}",
                reporter=f"{reporter.__class__.__module__}.{reporter.__class__.__name__}",
            )
            for obj in pipeline_objects
        ]

        for res in pipeline_results:
            reporter.report_pipeline_result(
                res, PipelineTaskStatus.PENDING, "Pipeline is waiting to start"
            )

        # build the task execution objects
        # cant use bulk create here as it doesnt populate the id on some databases
        # https://docs.djangoproject.com/en/4.2/ref/models/querysets/#bulk-create
        task_executions = [
            TaskExecution.objects.create(
                pipeline_result=pipeline_result,
                pipeline_task=task.pipeline_task,
                task_id=task.task_id,
                config=task.cleaned_config.dict(),
            )
            for (pipeline_result, task) in product(
                pipeline_results, pipeline.tasks.values()
            )
        ]

        for exe in task_executions:
            reporter.report_task_execution(
                exe, PipelineTaskStatus.PENDING, "Task is waiting to start"
            )

        # build the task results objects
        for task_execution in task_executions:
            task = task_execution.get_task()

            task_iterator = task.get_iterator()
            task_objects = task_iterator if task_iterator is not None else [None]

            for obj in task_objects:
                res = TaskResult.objects.create(
                    execution=task_execution,
                    serializable_task_object=task.get_serializable_task_object(obj),
                )
                reporter.report_task_result(
                    res, PipelineTaskStatus.PENDING, "Task is waiting to start"
                )

        return execution

    def get_pipeline_execution(self, _id):
        return PipelineExecution.objects.get(id=_id)

    def get_pipeline_result(self, _id):
        return PipelineResult.objects.get(id=_id)

    def get_task_execution(self, _id):
        return TaskExecution.objects.get(id=_id)

    def get_task_result(self, _id):
        return TaskResult.objects.get(id=_id)
