from typing import Any, Dict, List, Optional, Type

from django.utils import timezone

from pydantic import BaseModel, ValidationError

from ..log import logger
from ..reporters import BasePipelineReporter
from ..status import PipelineTaskStatus
from .registry import task_registry


class BaseTaskConfig(BaseModel):
    parents: List[
        str
    ] = (
        []
    )  # task ids that are required to have finished before this task can be started


class BaseTask:
    title: Optional[str] = ""
    ConfigType: Type[BaseTaskConfig] = BaseTaskConfig
    InputType: Optional[Type[BaseModel]] = None  # todo: can this a django form which can then be rendered?

    name: Optional[str] = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        task_registry.register(cls)

    def __init__(
        self,
        task_id: str,
        config: Dict[str, Any],
    ):
        self.task_id = task_id
        self.slug = task_registry.get_slug(self.__module__, self.__class__.__name__)
        self.cleaned_config = self.clean_config(config)

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
        pipeline_id: str,
        run_id: str,
        input_data: Dict[str, Any],
        reporter: BasePipelineReporter,
    ):
        try:
            cleaned_data = self.clean_input_data(input_data)
            logger.debug(cleaned_data)

            reporter.report_task(
                self.task_id,
                PipelineTaskStatus.RUNNING,
                "Task is running",
            )

            # record the task is running
            result = self.save(
                pipeline_id=pipeline_id,
                run_id=run_id,
                status=PipelineTaskStatus.RUNNING,
                input_data=cleaned_data.json(),
                started=timezone.now(),
            )

            # run the task
            output_data = self.run(cleaned_data)

            # update the result
            result.status = PipelineTaskStatus.DONE
            result.output_data = output_data
            result.completed = timezone.now()
            result.save()

            reporter.report_task(
                self.task_id,
                PipelineTaskStatus.DONE,
                "Done",
            )

            return True
        except InputValidationError as e:
            # If there is an error in the input data record the error
            reporter.report_task(
                self.slug,
                PipelineTaskStatus.VALIDATION_ERROR,
                e.msg,
            )

        except Exception as e:
            # If there is an error running the task record the error
            reporter.report_task(self.slug, PipelineTaskStatus.RUNTIME_ERROR, str(e))

        return False

    def run(
        self,
        cleaned_data: Optional[BaseModel],
    ):  # pragma: no cover
        pass

    def save(self, pipeline_id, run_id, status, started, input_data=None):
        from ..models import TaskResult

        defaults = dict(status=status, input_data=input_data, started=started)
        result, _ = TaskResult.objects.update_or_create(
            pipeline_id=pipeline_id, task_id=self.task_id, run_id=run_id, defaults=defaults
        )

        return result


class BaseTaskError(Exception):
    def __init__(self, task: BaseTask, msg: str):
        super().__init__(msg)
        self.task = task
        self.msg = msg


class ConfigValidationError(BaseTaskError):
    pass


class InputValidationError(BaseTaskError):
    pass
