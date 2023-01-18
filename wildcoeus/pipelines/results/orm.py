import uuid
from itertools import product
from typing import Dict, Any

from wildcoeus.pipelines.base import Pipeline
from wildcoeus.pipelines.models import PipelineExecution, PipelineResult, TaskExecution, TaskResult
from wildcoeus.pipelines.reporters import PipelineReporter
from wildcoeus.pipelines.results.base import BasePipelineResultsStorage
from wildcoeus.pipelines.runners import PipelineRunner


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
        )

        # build the pipeline results objects
        pipeline_iterator = pipeline.get_iterator()
        pipeline_objects = pipeline_iterator if pipeline_iterator is not None else [None]
        pipeline_results = PipelineResult.objects.bulk_create(
            PipelineResult(
                execution=execution,
                serializable_pipeline_object=pipeline.get_serializable_pipeline_object(obj),
                input_data=input_data,
                runner=f"{runner.__class__.__module__}.{runner.__class__.__name__}",
                reporter=f"{reporter.__class__.__module__}.{reporter.__class__.__name__}",
            ) for obj in pipeline_objects
        )

        # build the task execution objects
        task_executions = TaskExecution.objects.bulk_create(
            TaskExecution(
                pipeline_result=pipeline_result,
                pipeline_task=task.pipeline_task,
                task_id=task.task_id,
                config=task.cleaned_config.dict(),
            ) for (pipeline_result, task) in product(pipeline_results, pipeline.tasks.values())
        )

        # build the task results objects
        for task_execution in task_executions:
            task = task_execution.get_task(reporter)

            task_iterator = task.get_iterator()
            task_objects = task_iterator if task_iterator is not None else [None]

            for obj in task_objects:
                TaskResult.objects.create(
                    execution=task_execution,
                    serializable_task_object=task.get_serializable_task_object(obj),
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
