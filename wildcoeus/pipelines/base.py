from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, cast

from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model
from django.utils import timezone

from wildcoeus.meta import ClassWithAppConfigMeta
from wildcoeus.registry.registry import Registerable


if TYPE_CHECKING:  # pragma: nocover
    from wildcoeus.pipelines.runners import PipelineRunner

from wildcoeus.pipelines.models import PipelineExecution
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


class Pipeline(Registerable, ClassWithAppConfigMeta):
    tasks: Optional[dict[str, Task]] = {}

    def __init__(self):
        self.id = self.get_id()
        self.cleaned_tasks: List[Optional[Task]] = []

    def __str__(self):
        return self._meta.verbose_name

    @classmethod
    def postprocess_meta(cls, current_class_meta, resolved_meta_class):
        # collect all the components from all the base classes
        cls.tasks = {}
        for base in reversed(cls.__bases__):
            if not hasattr(base, "tasks") or not isinstance(base.tasks, dict):
                continue

            for k, v in ((k, v) for k, v in base.tasks.items() if isinstance(v, Task)):
                cls.tasks[k] = v

        # add all components from the current class
        for k, v in ((k, v) for k, v in cls.__dict__.items() if isinstance(v, Task)):
            cls.tasks[k] = v

        for key, task in list(cls.tasks.items()):
            task.pipeline_task = key

        return super().postprocess_meta(current_class_meta, resolved_meta_class)

    def clean_parents(
        self,
        task: Task,
        reporter: PipelineReporter,
        run_id: str,
    ):
        # check against pipeline keys, as parent is relative to the Pipeline, not Task.id which will is
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
                run_id=run_id,
                status=PipelineTaskStatus.CONFIG_ERROR.value,
                message="One or more of the parent ids are not in the pipeline",
            )
            return None

        return task

    def clean_tasks(
        self, reporter: "PipelineReporter", run_id: str
    ) -> List[Optional["Task"]]:
        """
        check that all configs with parents have a task with the parent label present
        """
        return list(
            map(
                lambda t: self.clean_parents(t, reporter, run_id) if t else t,
                self.tasks.values() if self.tasks else {},
            )
        )

    @classmethod
    def get_id(cls):
        """
        generate id based on where the pipeline is created
        """
        return "{}.{}".format(cls.__module__, cls.__name__)

    @classmethod
    def get_iterator(cls):
        """
        Pipelines can iterate over an object to run multiple times.
        """
        return None

    @staticmethod
    def get_serializable_pipeline_object(obj):
        if obj is None:
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
    ):
        iterator = self.get_iterator()

        res = True
        if iterator is not None:
            for pipeline_object in iterator:
                try:
                    res = (
                        self.start_pipeline(
                            run_id=run_id,
                            input_data=input_data,
                            runner=runner,
                            reporter=reporter,
                            pipeline_object=pipeline_object,
                        )
                        and res
                    )
                except Exception as e:
                    reporter.report_pipeline(
                        self.id,
                        PipelineTaskStatus.RUNTIME_ERROR.value,
                        f"Error starting pipeline: {e}",
                        run_id=run_id,
                        serializable_pipeline_object=self.get_serializable_pipeline_object(
                            obj=pipeline_object
                        ),
                    )
        else:
            try:
                res = self.start_pipeline(
                    run_id=run_id,
                    input_data=input_data,
                    runner=runner,
                    reporter=reporter,
                )
            except Exception as e:
                reporter.report_pipeline(
                    self.id,
                    PipelineTaskStatus.RUNTIME_ERROR.value,
                    f"Error starting pipeline: {e}",
                    run_id=run_id,
                )

        return res

    def start_pipeline(
        self,
        run_id: str,
        input_data: Dict[str, Any],
        runner: "PipelineRunner",
        reporter: "PipelineReporter",
        pipeline_object: Optional[Any] = None,
    ) -> bool:

        serializable_pipeline_object = self.get_serializable_pipeline_object(
            obj=pipeline_object
        )

        runner._report_pipeline_pending(
            pipeline_id=self.id,
            run_id=run_id,
            serializable_pipeline_object=serializable_pipeline_object,
            reporter=reporter,
        )

        # save that the pipeline has been triggered to run
        self.save(
            run_id=run_id,
            serializable_pipeline_object=serializable_pipeline_object,
            status=PipelineTaskStatus.PENDING.value,
            input_data=input_data,
            runner=runner.__class__.__name__,
            reporter=reporter.__class__.__name__,
        )

        self.cleaned_tasks = self.clean_tasks(reporter, run_id)

        if any(t is None for t in self.cleaned_tasks):
            # if any of the tasks have an invalid config cancel all others
            self.handle_error(
                reporter=reporter,
                serializable_pipeline_object=serializable_pipeline_object,
                run_id=run_id,
            )
            return False
        else:
            cleaned_tasks = cast(List[Task], self.cleaned_tasks)
            # else mark them all as pending
            for task in cleaned_tasks:
                # log task is queued
                reporter.report_task(
                    pipeline_task=task.pipeline_task,
                    task_id=task.task_id,
                    run_id=run_id,
                    status=PipelineTaskStatus.PENDING.value,
                    message="Task is waiting to start",
                )

        # save that the pipeline is set to run
        self.save(
            run_id=run_id,
            serializable_pipeline_object=serializable_pipeline_object,
            status=PipelineTaskStatus.RUNNING.value,
            started=timezone.now(),
        )

        # trigger runner to start
        started = runner.start(
            pipeline_id=self.id,
            run_id=run_id,
            tasks=cleaned_tasks,
            input_data=input_data,
            reporter=reporter,
            pipeline_object=pipeline_object,
        )

        return started

    def save(
        self,
        run_id: str,
        serializable_pipeline_object: Optional[Dict[str, Any]],
        **defaults,
    ):

        lookup = dict(
            pipeline_id=self.id,
            run_id=run_id,
        )
        if serializable_pipeline_object:
            lookup["serializable_pipeline_object"] = serializable_pipeline_object

        PipelineExecution.objects.update_or_create(**lookup, defaults=defaults)

    def handle_error(
        self,
        reporter,
        run_id: str,
        serializable_pipeline_object: Optional[Dict[str, Any]],
    ):
        # if any of the tasks have an invalid config cancel all others
        for task in (t for t in self.cleaned_tasks if t is not None):
            reporter.report_task(
                pipeline_task=task.pipeline_task,
                task_id=task.task_id,
                run_id=run_id,
                status=PipelineTaskStatus.CANCELLED.value,
                message="Tasks cancelled due to an error in the pipeline config",
            )
        # update that pipeline has been cancelled
        self.save(
            run_id,
            serializable_pipeline_object=serializable_pipeline_object,
            status=PipelineTaskStatus.CANCELLED.value,
        )


class ModelPipeline(Pipeline):
    _meta: Type["ModelPipeline.Meta"]

    class Meta:
        model: Optional[Model] = None

    def get_queryset(self, *args, **kwargs):
        if self._meta.model is not None:
            queryset = self._meta.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(self)s is missing a QuerySet. Define "
                "%(self)s.model or override "
                "%(self)s.get_queryset()." % {"self": self.__class__.__name__}
            )

        return queryset

    def get_iterator(self):
        return self.get_queryset()

    @staticmethod
    def get_serializable_pipeline_object(obj):
        if not obj:
            return None

        return {
            "pk": obj.pk,
            "app_label": obj._meta.app_label,
            "model_name": obj._meta.model_name,
        }
