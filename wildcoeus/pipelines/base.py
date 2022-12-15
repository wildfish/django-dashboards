from typing import TYPE_CHECKING, Any, Dict, List, Optional, cast

from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from django.utils import timezone


if TYPE_CHECKING:  # pragma: nocover
    from wildcoeus.pipelines.runners import PipelineRunner

from wildcoeus.pipelines.registry import pipeline_registry
from wildcoeus.pipelines.reporters.base import PipelineReporter
from wildcoeus.pipelines.status import PipelineTaskStatus
from wildcoeus.pipelines.tasks.base import Task


class PipelineType(type):
    def __new__(mcs, name, bases, attrs):
        """
        Collect tasks from attributes.
        """

        attrs["tasks"] = {}
        for key, value in list(attrs.items()):
            if isinstance(value, Task):
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


class Pipeline(metaclass=PipelineType):
    title: str = ""
    tasks: Optional[dict[str, Task]] = {}

    def __init__(self):
        self.id = pipeline_registry.get_slug(self.__module__, self.__class__.__name__)
        self.cleaned_tasks: List[Optional[Task]] = []

    class Meta:
        title: str

    def clean_parents(
        self,
        task: Task,
        reporter: PipelineReporter,
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
                status=PipelineTaskStatus.CONFIG_ERROR.value,
                message="One or more of the parent ids are not in the pipeline",
            )
            return None

        return task

    def clean_tasks(self, reporter: "PipelineReporter") -> List[Optional["Task"]]:
        """
        check that all configs with parents have a task with the parent label present
        """
        return list(
            map(
                lambda t: self.clean_parents(t, reporter) if t else t,
                self.tasks.values() if self.tasks else {},
            )
        )

    @classmethod
    def get_iterator(cls):
        """
        Pipelines can iterate over an object to run multiple times.
        """
        return None

    @staticmethod
    def get_serializable_pipeline_object(obj):
        if not obj:
            return None

        return {
            "obj": obj,
        }

    def start(
        self,
        run_id: str,
        input_data: Dict[str, Any],
        runner: "PipelineRunner",
        reporter: "PipelineReporter",
    ) -> bool:
        reporter.report_pipeline(
            pipeline_id=self.id,
            status=PipelineTaskStatus.PENDING.value,
            message="Pipeline is waiting to start",
        )

        # save that the pipeline has been triggered to run
        self.save(
            run_id=run_id,
            status=PipelineTaskStatus.PENDING.value,
            input_data=input_data,
            runner=runner.__class__.__name__,
            reporter=reporter.__class__.__name__,
        )

        self.cleaned_tasks = self.clean_tasks(reporter)

        if any(t is None for t in self.cleaned_tasks):
            # if any of the tasks have an invalid config cancel all others
            self.handle_error(reporter=reporter, run_id=run_id)
            return False
        else:
            cleaned_tasks = cast(List[Task], self.cleaned_tasks)
            # else mark them all as pending
            for task in cleaned_tasks:
                # log task is queued
                reporter.report_task(
                    pipeline_task=task.pipeline_task,
                    task_id=task.task_id,
                    status=PipelineTaskStatus.PENDING.value,
                    message="Task is waiting to start",
                )
                # save that each task is pending
                task.save(
                    pipeline_id=self.id,
                    run_id=run_id,
                    status=PipelineTaskStatus.PENDING.value,
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
            status=PipelineTaskStatus.RUNNING.value,
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

    def save(self, run_id: str, **defaults):
        from .models import PipelineExecution

        PipelineExecution.objects.update_or_create(
            pipeline_id=self.id, run_id=run_id, defaults=defaults
        )

    def handle_error(self, reporter, run_id):
        # if any of the tasks have an invalid config cancel all others
        for task in (t for t in self.cleaned_tasks if t is not None):
            reporter.report_task(
                pipeline_task=task.pipeline_task,
                task_id=task.task_id,
                status=PipelineTaskStatus.CANCELLED.value,
                message="Tasks cancelled due to an error in the pipeline config",
            )
        # update that pipeline has been cancelled
        self.save(run_id, status=PipelineTaskStatus.CANCELLED.value)


class ModelPipeline(Pipeline):
    class Meta:
        title: str
        model: Optional[str]
        queryset = Optional[str]

    @classmethod
    def get_queryset(cls):
        """
        Return the list of items for this pipeline to run against.
        """
        if getattr(cls.Meta, "queryset", None) is not None:
            queryset = cls.Meta.queryset
            if isinstance(queryset, QuerySet):
                queryset = queryset.all()
        elif cls.Meta.model is not None:
            queryset = cls.Meta.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {"cls": cls.__class__.__name__}
            )

        return queryset

    @classmethod
    def get_iterator(cls):
        return cls.get_queryset()

    @staticmethod
    def get_serializable_pipeline_object(obj):
        if not obj:
            return None

        return {
            "pk": obj.pk,
            "app_label": obj._meta.app_label,
            "model_name": obj._meta.model_name,
        }
