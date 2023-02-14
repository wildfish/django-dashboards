from typing import Any, Dict, List, Optional, Type

from django.core.exceptions import ImproperlyConfigured

from pydantic import BaseModel, Extra, ValidationError

from wildcoeus.meta import ClassWithAppConfigMeta
from wildcoeus.pipelines.reporters import PipelineReporter
from wildcoeus.pipelines.results.base import TaskResult
from wildcoeus.pipelines.status import PipelineTaskStatus
from wildcoeus.pipelines.tasks.registry import task_registry
from wildcoeus.registry.registry import Registerable


class TaskConfig(BaseModel):
    parents: List[
        str
    ] = (
        []
    )  # task ids that are required to have finished before this task can be started

    class Config:
        extra = Extra.allow


class Task(Registerable, ClassWithAppConfigMeta):
    pipeline_task: str  # The attribute this tasks is named against - set via __new__ on Pipeline
    title: Optional[str] = ""
    ConfigType: Type[TaskConfig] = TaskConfig
    InputType: Optional[
        Type[BaseModel]
    ] = None  # todo: can this a django form which can then be rendered?

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not cls._meta.abstract:
            task_registry.register(cls)

    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
    ):
        self.task_id = self.get_id()
        self._config = config or {}
        self.cleaned_config = self.clean_config(config or {})
        self.pipeline_object = None
        self.task_object = None

    @classmethod
    def get_iterator(cls):
        """
        Pipelines can iterate over an object to run multiple times.
        """
        return None

    @staticmethod
    def get_serializable_task_object(obj):
        if obj is None:
            return None

        return {
            "obj": obj,
        }

    @classmethod
    def get_object(
        cls,
        serializable_object: Dict[str, Any],
    ):
        from wildcoeus.pipelines.utils import get_object

        return get_object(serializable_object)

    def clean_config(self, config: Dict[str, Any]):
        try:
            model = self.ConfigType(**(config or {}))
            return model
        except ValidationError as e:
            raise ConfigValidationError(self, e.json(indent=False))

    def clean_input_data(self, input_data: Dict[str, Any]):
        if input_data and self.InputType is None:
            raise InputValidationError(
                self, "Input data was provided when no input type was specified"
            )

        if self.InputType is None:
            return None

        try:
            model = self.InputType(**(input_data or {}))
            return model
        except ValidationError as e:
            raise InputValidationError(self, e.json(indent=False))

    def start(
        self,
        task_result: TaskResult,
        reporter: PipelineReporter,
    ):
        try:
            task_result.report_status_change(reporter, PipelineTaskStatus.RUNNING)

            self.pipeline_object = self.get_object(
                task_result.get_serializable_pipeline_object()
            )
            self.task_object = self.get_object(
                task_result.get_serializable_task_object()
            )

            # run the task
            self.run(
                pipeline_id=task_result.get_pipeline_id(),
                run_id=task_result.get_run_id(),
                cleaned_data=task_result.get_task().clean_input_data(
                    task_result.get_input_data()
                ),
            )

            # update the result as completed
            task_result.report_status_change(
                reporter, PipelineTaskStatus.DONE, propagate=False
            )

            return True
        except (InputValidationError, Exception) as e:
            status = (
                PipelineTaskStatus.VALIDATION_ERROR
                if isinstance(e, InputValidationError)
                else PipelineTaskStatus.RUNTIME_ERROR
            )
            task_result.report_status_change(reporter, status, message=str(e))
            raise

    def run(
        self,
        pipeline_id: str,
        run_id: str,
        cleaned_data: Optional[BaseModel],
    ):  # pragma: no cover
        raise NotImplementedError("run not implemented")

    @classmethod
    def get_id(cls):
        return "{}.{}".format(cls._meta.app_label, cls.__name__)


class ModelTask(Task):
    class Meta:
        model: Optional[str]

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
    def get_serializable_task_object(obj):
        if not obj:
            return None

        return {
            "pk": obj.pk,
            "app_label": obj._meta.app_label,
            "model_name": obj._meta.model_name,
        }


class TaskError(Exception):
    def __init__(self, task: Task, msg: str):
        super().__init__(msg)
        self.task = task
        self.msg = msg


class ConfigValidationError(TaskError):
    pass


class InputValidationError(TaskError):
    pass
