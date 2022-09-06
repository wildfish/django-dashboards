from typing import Any, Dict, List, Optional, Type

from pydantic import BaseModel, ValidationError

from ..reporters import BasePipelineReporter, PipelineTaskStatus
from .registry import task_registry


class BaseTaskConfig(BaseModel):
    title: Optional[str]  # human readable name for displaying
    label: Optional[str]  # label will be used to specify dependencies
    parents: Optional[
        List[str]
    ]  # task labels that are required to have finished before this task can be started


class BaseTask:
    ConfigType: Optional[Type[BaseTaskConfig]] = None
    cleaned_config: Optional[BaseTaskConfig]

    InputType: Optional[Type[BaseModel]] = None

    name: Optional[str] = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        task_registry.register(cls)

    def __init__(
        self,
        task_id: str,
        reporter: BasePipelineReporter,
        config: Optional[Dict[str, Any]] = None,
    ):
        self.id = task_id
        self.reporter = reporter
        self.cleaned_config = self.clean_config(config)

    def clean_config(self, config: Optional[Dict[str, Any]]):
        if config and self.ConfigType is None:
            raise ConfigValidationError(
                self, "Config was provided no config type was specified"
            )

        if self.ConfigType is None:
            return None

        try:
            model = self.ConfigType(**(config or {}))
            return model
        except ValidationError as e:
            raise ConfigValidationError(self, e.json(indent=False))

    def clean_input_data(self, input_data: Optional[Dict[str, Any]]):
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

    def start(self, input_data: Dict[str, Any]):
        try:
            cleaned_data = self.clean_input_data(input_data)
            self.reporter.report_task(
                self.id,
                PipelineTaskStatus.RUNNING,
                "Task is running",
            )
            self.run(cleaned_data)
        except InputValidationError as e:
            self.reporter.report_task(
                self.id,
                PipelineTaskStatus.VALIDATION_ERROR,
                e.msg,
            )

    def run(
        self,
        cleaned_data: Optional[BaseModel],
    ):  # pragma: no cover
        pass


class BaseTaskError(Exception):
    def __init__(self, task: BaseTask, msg: str):
        super().__init__(msg)
        self.task = task
        self.msg = msg


class ConfigValidationError(BaseTaskError):
    pass


class InputValidationError(BaseTaskError):
    pass
