from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type

from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model

from wildcoeus.meta import ClassWithAppConfigMeta
from wildcoeus.pipelines.results.base import BasePipelineExecution
from wildcoeus.pipelines.results.helpers import build_pipeline_execution
from wildcoeus.registry.registry import Registerable


if TYPE_CHECKING:  # pragma: nocover
    from wildcoeus.pipelines.runners import PipelineRunner
    from wildcoeus.pipelines.reporters.base import PipelineReporter

from wildcoeus.pipelines.status import PipelineTaskStatus
from wildcoeus.pipelines.tasks.base import Task


class Pipeline(Registerable, ClassWithAppConfigMeta):
    tasks: Optional[dict[str, Task]] = {}
    ordering: Optional[dict[str, List[str]]] = None

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
        reporter: "PipelineReporter",
        runner: "PipelineRunner",
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
            pipeline_execution = build_pipeline_execution(
                self,
                run_id,
                runner,
                reporter,
                {},
                build_all=None,
            )
            reporter.report_pipeline_execution(
                pipeline_execution,
                PipelineTaskStatus.CONFIG_ERROR,
                "One or more of the parent ids are not in the pipeline",
            )
            # TODO: make this a propper exception and make the message relate to the bad task
            raise Exception("One or more of the parent ids are not in the pipeline")

        return task

    def clean_tasks(
        self, reporter: "PipelineReporter", runner: "PipelineRunner", run_id: str
    ) -> List[Optional["Task"]]:
        """
        check that all configs with parents have a task with the parent label present
        """
        return list(
            map(
                lambda t: self.clean_parents(t, reporter, runner, run_id) if t else t,
                self.tasks.values() if self.tasks else {},
            )
        )

    @classmethod
    def get_id(cls):
        """
        generate id based on where the pipeline is created
        """
        return "{}.{}".format(cls._meta.app_label, cls.__name__)

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
        self.cleaned_tasks = self.clean_tasks(reporter, runner, run_id)

        # create the execution object to store all pipeline results against
        execution = build_pipeline_execution(self, run_id, runner, reporter, input_data)

        if any(t is None for t in self.cleaned_tasks):
            # if any of the tasks have an invalid config cancel all others
            self.handle_error(execution, reporter)
            return False

        return self.start_pipeline(
            execution,
            runner=runner,
            reporter=reporter,
        )

    def start_pipeline(
        self,
        pipeline_execution: BasePipelineExecution,
        runner: "PipelineRunner",
        reporter: "PipelineReporter",
    ) -> bool:
        # trigger runner to start
        started = runner.start(
            pipeline_execution,
            reporter=reporter,
        )

        return started

    def handle_error(
        self,
        execution: BasePipelineExecution,
        reporter,
    ):
        # update that pipeline has been cancelled
        execution.report_status_change(
            reporter,
            PipelineTaskStatus.CANCELLED,
            message="Pipeline cancelled due to an error in the pipeline config",
        )

        # cancel all pipeline results
        for pipeline_result in execution.get_pipeline_results():
            pipeline_result.report_status_change(
                reporter,
                PipelineTaskStatus.CANCELLED,
                message="Pipeline cancelled due to an error in the pipeline config",
                propagate=False,
            )

            # report all task executions have been cancelled
            for task_execution in pipeline_result.get_task_executions():
                task_execution.report_status_change(
                    reporter,
                    PipelineTaskStatus.CANCELLED,
                    message="Tasks cancelled due to an error in the pipeline config",
                    propagate=False,
                )

                # report all task results have been cancelled
                for task_result in task_execution.get_task_results():
                    task_result.report_status_change(
                        reporter,
                        PipelineTaskStatus.CANCELLED,
                        message="Tasks cancelled due to an error in the pipeline config",
                        propagate=False,
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
