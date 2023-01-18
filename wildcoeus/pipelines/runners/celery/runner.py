from celery import chain, signature, chord

from wildcoeus.pipelines.reporters import PipelineReporter
from wildcoeus.pipelines.runners import PipelineRunner
from wildcoeus.pipelines.status import PipelineTaskStatus

from .tasks import run_pipeline_result_report, run_task, run_task_result_report, run_pipeline_execution_report,\
    run_task_execution_report
from ...results.base import BasePipelineExecution, BasePipelineResult, BaseTaskResult, BaseTaskExecution


class Runner(PipelineRunner):
    @classmethod
    def _build_celery_task(cls, task: BaseTaskResult):
        celery_task = run_task.si(task.id)
        celery_task.link_error(
            run_task_result_report.si(
                task_result_id=task.id,
                status=PipelineTaskStatus.RUNTIME_ERROR.value,
                message="Task Error",
            )
        )

        # set to queue if defined in config
        celery_task.set(queue=getattr(task.get_task(), "celery_queue", None))

        return celery_task

    @classmethod
    def _expand_celery_tasks(
        cls,
        task: BaseTaskExecution,
    ) -> signature:
        """
        Start a task async. Task reports will be inline however, we add a link error incase
        anything occurs above task.
        """
        return chord(
            [
                cls._build_celery_task(result)
                for result in task.get_task_results()
            ],
            run_task_execution_report.si(
                task_execution_id=task.id,
                status=PipelineTaskStatus.DONE.value,
                message="Done",
            )
        )

    def _build_pipeline_chain(self, pipeline_result: BasePipelineResult):
        ordered_tasks = self._get_task_graph(pipeline_result)

        c = chain(
            # Report starting
            run_pipeline_result_report.si(
                pipeline_result_id=pipeline_result.id,
                status=PipelineTaskStatus.RUNNING.value,
                message="Running",
                propagate=True,
            ),
            # Run tasks in graph order
            *map(
                lambda t: self._expand_celery_tasks(t),
                ordered_tasks,
            ),
            # Report Done
            run_pipeline_result_report.si(
                pipeline_result_id=pipeline_result.id,
                status=PipelineTaskStatus.DONE.value,
                message="Done",
                propagate=False,
            ),
        )
        c.link_error(
            # Report pipeline error
            run_pipeline_result_report.si(
                pipeline_result_id=pipeline_result.id,
                status=PipelineTaskStatus.CANCELLED.value,
                message="Pipeline Error - remaining tasks cancelled",
                propagate=True,
            )
        )

        return c

    def start_runner(
        self,
        pipeline_execution: BasePipelineExecution,
        reporter: PipelineReporter,
    ) -> bool:
        # build a chord that runs each pipeline result
        # and processes the final state of the pipeline
        c = chord(
            [
                self._build_pipeline_chain(pipeline_result)
                for pipeline_result in pipeline_execution.get_pipeline_results()
            ],
            run_pipeline_execution_report.si(
                pipeline_execution_id=pipeline_execution.id,
                status=PipelineTaskStatus.DONE.value,
                message="Done",
            )
        )

        return c()
