from datetime import datetime
from itertools import product
from typing import Any, Dict, Optional, Sequence

from django.db.models import Avg, Count, F, Max, Q

from wildcoeus.pipelines.base import Pipeline
from wildcoeus.pipelines.models import (
    OrmPipelineExecution,
    OrmPipelineResult,
    OrmTaskExecution,
    OrmTaskResult,
)
from wildcoeus.pipelines.reporters import PipelineReporter
from wildcoeus.pipelines.results.base import (
    PipelineDigest,
    PipelineDigestItem,
    PipelineResult,
    PipelineResultsStorage,
    TaskExecution,
    TaskResult,
)
from wildcoeus.pipelines.runners import PipelineRunner
from wildcoeus.pipelines.status import PipelineTaskStatus


class OrmPipelineResultsStorage(PipelineResultsStorage):
    """
    Class to store pipeline results in the django ORM
    """

    def _get_pipeline_execution_qs(self):
        return OrmPipelineExecution.objects.with_extra_stats()

    def _get_pipeline_result_qs(self):
        return OrmPipelineResult.objects.with_extra_stats()

    def _get_task_execution_qs(self):
        return OrmTaskExecution.objects.all()

    def _get_task_result_qs(self):
        return OrmTaskResult.objects.all()

    def build_pipeline_execution(
        self,
        pipeline: Pipeline,
        run_id: str,
        runner: PipelineRunner,
        reporter: PipelineReporter,
        input_data: Dict[str, Any],
        build_all=True,
    ):
        execution = OrmPipelineExecution.objects.create(
            pipeline_id=pipeline.id,
            run_id=run_id,
            input_data=input_data,
        )
        reporter.report_pipeline_execution(
            execution, PipelineTaskStatus.PENDING, "Pipeline is waiting to start"
        )

        if not build_all:
            return execution

        # build the pipeline results objects
        pipeline_iterator = pipeline.get_iterator()
        pipeline_objects = (
            pipeline_iterator if pipeline_iterator is not None else [None]
        )

        # cant use bulk create here as it doesnt populate the id on some databases
        # https://docs.djangoproject.com/en/4.2/ref/models/querysets/#bulk-create
        pipeline_results = [
            OrmPipelineResult.objects.create(
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
            OrmTaskExecution.objects.create(
                pipeline_result=pipeline_result,
                pipeline_task=task.pipeline_task,
                task_id=task.task_id,
                config=task.cleaned_config.dict(),
            )
            for (pipeline_result, task) in product(
                pipeline_results, (pipeline.tasks or {}).values()
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
                res = OrmTaskResult.objects.create(
                    execution=task_execution,
                    serializable_task_object=task.get_serializable_task_object(obj),
                )
                reporter.report_task_result(
                    res, PipelineTaskStatus.PENDING, "Task is waiting to start"
                )

        return execution

    def get_pipeline_digest(self) -> PipelineDigest:
        qs = (
            OrmPipelineResult.objects.values("execution__pipeline_id")
            .annotate(
                total_success=Count(
                    "id", filter=Q(status=PipelineTaskStatus.DONE.value)
                ),
                total_failure=Count(
                    "id", filter=Q(status__in=PipelineTaskStatus.failed_statuses())
                ),
                last_ran=Max("started"),
                average_runtime=Avg(F("completed") - F("started")),
                pipeline_id=F("execution__pipeline_id"),
            )
            .order_by("pipeline_id")
        )

        return {
            v["pipeline_id"]: PipelineDigestItem(
                last_ran=v["last_ran"],
                average_runtime=v["average_runtime"],
                total_success=v["total_success"],
                total_failure=v["total_failure"],
                total_runs=v["total_success"] + v["total_failure"],
            )
            for v in qs
        }

    def get_pipeline_executions(self, pipeline_id: Optional[str] = None):
        qs = self._get_pipeline_execution_qs()

        if pipeline_id:
            qs = qs.filter(pipeline_id=pipeline_id)

        return qs

    def get_pipeline_execution(self, run_id):
        return self._get_pipeline_execution_qs().filter(run_id=run_id).first()

    def get_pipeline_results(
        self, run_id: Optional[str] = None
    ) -> Sequence[PipelineResult]:
        qs = self._get_pipeline_result_qs()

        if run_id:
            qs = qs.filter(execution__run_id=run_id).distinct()

        return qs

    def get_pipeline_result(self, _id):
        return self._get_pipeline_result_qs().filter(id=_id).first()

    def get_task_executions(
        self,
        run_id: Optional[str] = None,
        pipeline_result_id: Optional[str] = None,
    ) -> Sequence[TaskExecution]:
        qs = self._get_task_execution_qs()

        if run_id:
            qs = qs.filter(pipeline_result__execution__run_id=run_id).distinct()

        if pipeline_result_id:
            qs = qs.filter(pipeline_result__id=pipeline_result_id).distinct()

        return qs

    def get_task_execution(self, _id):
        return self._get_task_execution_qs().filter(id=_id).first()

    def get_task_results(
        self,
        run_id: Optional[str] = None,
        pipeline_result_id: Optional[str] = None,
        task_execution_id: Optional[str] = None,
    ) -> Sequence[TaskResult]:
        qs = self._get_task_result_qs()

        if run_id:
            qs = qs.filter(
                execution__pipeline_result__execution__run_id=run_id
            ).distinct()

        if pipeline_result_id:
            qs = qs.filter(execution__pipeline_result__id=pipeline_result_id).distinct()

        if task_execution_id:
            qs = qs.filter(execution__id=task_execution_id).distinct()

        return qs

    def get_task_result(self, _id):
        return self._get_task_result_qs().filter(id=_id).first()

    def cleanup(self, before: Optional[datetime] = None):
        if before:
            run_ids = list(
                OrmPipelineExecution.objects.filter(started__lt=before).values_list(
                    "run_id", flat=True
                )
            )
        else:
            run_ids = list(
                OrmPipelineExecution.objects.values_list("run_id", flat=True)
            )

        if run_ids:
            OrmPipelineExecution.objects.filter(run_id__in=run_ids).delete()

        return run_ids
