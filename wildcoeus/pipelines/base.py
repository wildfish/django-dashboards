from typing import TYPE_CHECKING, Any, Dict, List, Optional, cast
from django.utils import timezone

if TYPE_CHECKING:  # pragma: nocover
    from wildcoeus.pipelines.runners import BasePipelineRunner

from wildcoeus.pipelines.registry import pipeline_registry
from wildcoeus.pipelines.reporters.base import BasePipelineReporter
from wildcoeus.pipelines.status import PipelineTaskStatus
from wildcoeus.pipelines.tasks.base import BaseTask


class PipelineType(type):
    def __new__(mcs, name, bases, attrs):
        """
        Collect tasks from attributes.
        """

        attrs["tasks"] = {}
        for key, value in list(attrs.items()):
            if isinstance(value, BaseTask):
                task = attrs.pop(key)
                task.pipeline_task = key
                attrs["tasks"][key] = task

        pipeline_class = super().__new__(mcs, name, bases, attrs)
        tasks = {}
        for base in reversed(pipeline_class.__mro__):
            # Collect tasks from base class.
            if hasattr(base, "tasks"):
                tasks.update(base.tasks)

            # Field shadowing.
            for attr, value in base.__dict__.items():
                if value is None and attr in tasks:
                    tasks.pop(attr)

        # add tasks to class.
        pipeline_class.tasks = tasks

        return pipeline_class


class BasePipeline(metaclass=PipelineType):
    title: str = ""
    tasks: Optional[dict[str, BaseTask]] = {}

    def __init__(self):
        self.id = pipeline_registry.get_slug(self.__module__, self.__class__.__name__)
        self.cleaned_tasks: List[Optional[BaseTask]] = []

    def clean_parents(
        self,
        task: BaseTask,
        reporter: BasePipelineReporter,
    ):
        # check against pipeline kets, as parent is relative to the Pipeline, not Task.id which will is
        # full task id.
        other_tasks = self.tasks.values() if self.tasks else []
        other_pipeline_tasks = [
            t.pipeline_task
            for t in other_tasks
            if t.pipeline_task != task.pipeline_task
        ]
        parent_keys = getattr(task.cleaned_config, "parents", []) or []

        if not all(p in other_pipeline_tasks for p in parent_keys):
            reporter.report_task(
                pipeline_task=task.pipeline_task,
                task_id=task.task_id,
                status=PipelineTaskStatus.CONFIG_ERROR,
                message="One or more of the parent ids are not in the pipeline",
            )
            return None

        return task

    def clean_tasks(
        self, reporter: "BasePipelineReporter"
    ) -> List[Optional["BaseTask"]]:
        """
        check that all configs with parents have a task with the parent label present
        """
        return list(
            map(
                lambda t: self.clean_parents(t, reporter) if t else t,
                self.tasks.values() if self.tasks else {},
            )
        )

    def start(
        self,
        run_id: str,
        input_data: Dict[str, Any],
        runner: "BasePipelineRunner",
        reporter: "BasePipelineReporter",
    ) -> bool:
        reporter.report_pipeline(
            pipeline_id=self.id,
            status=PipelineTaskStatus.PENDING,
            message="Pipeline is waiting to start",
        )

        # save that the pipeline has been triggered to run
        self.save(
            run_id=run_id,
            status=PipelineTaskStatus.PENDING.value,
            input_data=input_data,
            runner=runner.__class__.__name__,
            reporter=reporter.__class__.__name__
        )

        self.cleaned_tasks = self.clean_tasks(reporter)

        if any(t is None for t in self.cleaned_tasks):
            # if any of the tasks have an invalid config cancel all others
            self.handle_cancelled(run_id=run_id)
            return False
        else:
            cleaned_tasks = cast(List[BaseTask], self.cleaned_tasks)

            # else mark them all as pending
            for task in cleaned_tasks:
                # log task is queued
                reporter.report_task(
                    pipeline_task=task.pipeline_task,
                    task_id=task.task_id,
                    status=PipelineTaskStatus.PENDING,
                    message="Task is waiting to start",
                )
                # save that each task is pending
                task.save(
                    pipeline_id=self.id,
                    run_id=run_id,
                    status=PipelineTaskStatus.PENDING.value
                )

        # save that the pipeline is set to run
        self.save(
            run_id=run_id,
            status=PipelineTaskStatus.RUNNING.value,
            started=timezone.now(),
        )

        # record it is starting
        reporter.report_pipeline(
            pipeline_id=self.id,
            status=PipelineTaskStatus.RUNNING,
            message="Started",
        )

        # trigger runner to start
        started = runner.start(
            pipeline_id=self.id,
            run_id=run_id,
            tasks=cleaned_tasks,
            input_data=input_data,
            reporter=reporter,
        )

        return started

    def save(self, run_id: str, **defaults: dict):
        from .models import PipelineExecution
        PipelineExecution.objects.update_or_create(
            pipeline_id=self.id,
            run_id=run_id,
            defaults=defaults
        )

    def handle_cancelled(self, run_id):
        # if any of the tasks have an invalid config cancel all others
        for task in (t for t in self.cleaned_tasks if t is not None):
            reporter.report_task(
                pipeline_task=task.pipeline_task,
                task_id=task.task_id,
                status=PipelineTaskStatus.CANCELLED,
                message="Tasks cancelled due to an error in the pipeline config",
            )
        # update that pipeline has been cancelled
        self.save(run_id, status=PipelineTaskStatus.CANCELLED.value)
