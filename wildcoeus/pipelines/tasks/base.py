from typing import Any, Dict, List, Optional, Type

from django.utils import timezone

from pydantic import BaseModel, ValidationError

from wildcoeus.pipelines.log import logger
from wildcoeus.pipelines.reporters import PipelineReporter
from wildcoeus.pipelines.status import PipelineTaskStatus
from wildcoeus.pipelines.tasks.registry import task_registry


class TaskConfig(BaseModel):
    parents: List[
        str
    ] = (
        []
    )  # task ids that are required to have finished before this task can be started


class Task:
    pipeline_task: str  # The attribute this tasks is named against - set via __new__ on Pipeline
    title: Optional[str] = ""
    ConfigType: Type[TaskConfig] = TaskConfig
    InputType: Optional[
        Type[BaseModel]
    ] = None  # todo: can this a django form which can then be rendered?

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        task_registry.register(cls)

    def __init__(
        self,
        config: Dict[str, Any] = {},
    ):
        self.task_id = task_registry.get_task_id(
            self.__module__, self.__class__.__name__
        )
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
        reporter: PipelineReporter,
        instance_lookup: Optional[dict[str, Any]] = None,
    ):
        try:
            cleaned_data = self.clean_input_data(input_data)
            logger.debug(cleaned_data)

            reporter.report_task(
                pipeline_task=self.pipeline_task,
                task_id=self.task_id,
                status=PipelineTaskStatus.RUNNING,
                message="Task is running",
                instance_lookup=instance_lookup,
            )

            # record the task is running
            result = self.save(
                pipeline_id=pipeline_id,
                run_id=run_id,
                status=PipelineTaskStatus.RUNNING,
                started=timezone.now(),
                config=self.cleaned_config.dict() if self.cleaned_config else None,
                input_data=cleaned_data.dict() if cleaned_data else None,
            )

            # run the task
            self.run(pipeline_id, run_id, cleaned_data)

            # update the result as completed
            result.status = PipelineTaskStatus.DONE
            result.completed = timezone.now()
            result.save()

            reporter.report_task(
                pipeline_task=self.pipeline_task,
                task_id=self.task_id,
                status=PipelineTaskStatus.DONE,
                message="Done",
                instance_lookup=instance_lookup,
            )

            return True
        except InputValidationError as e:
            # If there is an error in the input data record the error
            reporter.report_task(
                pipeline_task=self.pipeline_task,
                task_id=self.task_id,
                status=PipelineTaskStatus.VALIDATION_ERROR,
                message=e.msg,
                instance_lookup=instance_lookup,
            )
        except Exception as e:
            # If there is an error running the task record the error
            reporter.report_task(
                pipeline_task=self.pipeline_task,
                task_id=self.task_id,
                status=PipelineTaskStatus.RUNTIME_ERROR,
                message=str(e),
                instance_lookup=instance_lookup,
            )

        return False

    def run(
        self,
        pipeline_id: str,
        run_id: str,
        cleaned_data: Optional[BaseModel],
    ):  # pragma: no cover
        raise NotImplementedError("run not implemented")

    def save(self, pipeline_id, run_id, status, started, config=None, input_data=None):
        from ..models import TaskResult

        logger.debug(config)
        logger.debug(type(config))
        logger.debug("*" * 40)

        defaults = dict(
            status=status, config=config, input_data=input_data, started=started
        )
        result, _ = TaskResult.objects.update_or_create(
            pipeline_id=pipeline_id,
            pipeline_task=self.pipeline_task,
            task_id=self.task_id,
            run_id=run_id,
            defaults=defaults,
        )

        return result


class ModelTask(Task):
    def __init__(
        self, content_type_id: int, object_id: int, config: Dict[str, Any] = {}
    ):
        self.content_type_id = content_type_id
        self.object_id = object_id
        super().__init__(config=config)

    def get_object(self):
        from django.contrib.contenttypes.models import ContentType

        object_type = ContentType.objects.get_for_id(self.content_type_id)
        obj = object_type.get_object_for_this_type(self.object_id)
        return obj


class TaskError(Exception):
    def __init__(self, task: Task, msg: str):
        super().__init__(msg)
        self.task = task
        self.msg = msg


class ConfigValidationError(TaskError):
    pass


class InputValidationError(TaskError):
    pass
