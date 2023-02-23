from celery import chain, chord, signature

from wildcoeus.pipelines.reporters import PipelineReporter
from wildcoeus.pipelines.runners import PipelineRunner
from wildcoeus.pipelines.status import PipelineTaskStatus

from ...results.base import PipelineExecution, PipelineResult, TaskExecution, TaskResult
from .tasks import (
    run_pipeline_execution_report,
    run_pipeline_result_report,
    run_task,
    run_task_execution_report,
    run_task_result_report,
)


class Runner(PipelineRunner):
    @classmethod
    def build_celery_task(cls, task: TaskResult):
        """
        Converts the task result into a celery signature. A signature is added to
        catch errors and record the status change on the results object. If the
        task config has a :code:`celery_queue` property the task will be assigned
        to that queue.

        :param task: The task result that represents the task to convert.
        """
        celery_task = run_task.si(task.get_id())
        celery_task.link_error(
            run_task_result_report.si(
                task_result_id=task.get_id(),
                status=PipelineTaskStatus.RUNTIME_ERROR.value,
                message="Task Error",
            )
        )

        # set to queue if defined in config
        celery_task.set(
            queue=getattr(task.get_task().cleaned_config, "celery_queue", None)
        )

        return celery_task

    @classmethod
    def expand_celery_tasks(
        cls,
        task: TaskExecution,
    ) -> signature:
        """
        Builds a celery chord or canvas based on the task execution. After all tasks
        instances are ran a task will be ran to update the task execution status.

        If the task has an iterable a chord will be generated to run each task instance
        in parallel. If there is no iterator a chain will be built.

        :param task: The task execution object to expand.
        """
        on_complete = run_task_execution_report.si(
            task_execution_id=task.id,
            status=PipelineTaskStatus.DONE.value,
            message="Done",
            propagate=False,
        )

        if len(task.get_task_results()) == 1:
            # build a chord that runs teh only task result
            # and processes the final state of the task result
            return chain(
                cls.build_celery_task(task.get_task_results()[0]),
                on_complete,
            )
        else:
            # build a chord that runs each task result
            # and processes the final state of the task result
            return chord(
                [cls.build_celery_task(result) for result in task.get_task_results()],
                on_complete,
            )

    def expand_pipeline_result(self, pipeline_result: PipelineResult):
        """
        Expands the pipeline into a celery canvas. Currently this builds a chain running
        each expanded task in series but will be updated to schedule tasks in parallel
        where possible.

        :param pipeline_result: The pipeline instance to expand
        """
        ordered_tasks = self.get_flat_task_list(pipeline_result)

        c = chain(
            # Report starting
            run_pipeline_result_report.si(
                pipeline_result_id=pipeline_result.get_id(),
                status=PipelineTaskStatus.RUNNING.value,
                message="Running",
                propagate=True,
            ),
            # Run tasks in graph order
            *map(
                lambda t: self.expand_celery_tasks(t),
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

    def expand_pipeline_execution(
        self,
        pipeline_execution: PipelineExecution,
    ):
        """
        Expands the pipeline execution into a celery canvas.  After all pipeline
        instances are ran a task will be ran to update the pipeline execution status.

        If the pipeline has an iterable a chord will be generated to run each pipeline instance
        in parallel. If there is no iterator a chain will be built.

        :param pipeline_execution: The pipeline execution object to expand.
        """
        on_complete = run_pipeline_execution_report.si(
            run_id=pipeline_execution.get_run_id(),
            status=PipelineTaskStatus.DONE.value,
            message="Done",
        )

        if len(pipeline_execution.get_pipeline_results()) == 1:
            # build a chord that runs the only pipeline result
            # and processes the final state of the pipeline
            return chain(
                self.expand_pipeline_result(pipeline_execution.get_pipeline_results()[0]),
                on_complete,
            )
        else:
            # build a chord that runs each pipeline result
            # and processes the final state of the pipeline
            return chord(
                [
                    self.expand_pipeline_result(pipeline_result)
                    for pipeline_result in pipeline_execution.get_pipeline_results()
                ],
                on_complete,
            )

    def run(
        self,
        pipeline_execution: PipelineExecution,
        reporter: PipelineReporter,
    ) -> bool:
        """
        Creates a celery canvas representing the pipeline and schedules it with the celery broker.

        Returns :code:`True` if the pipeline was scheduled successfully, :code:`False`
        otherwise. This has no guarantee on the completion of the pipeline, just that
        it has been successfully scheduled.

        :param pipeline_execution: The pipeline execution object representing the
            pipeline to run.
        :param reporter: The reporter object to write messages to.
        """
        return self.expand_pipeline_execution(pipeline_execution)()
