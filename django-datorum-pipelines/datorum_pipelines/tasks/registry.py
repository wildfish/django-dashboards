from typing import TYPE_CHECKING, Any, Dict, Type


if TYPE_CHECKING:  # pragma: no cover
    from .base import BaseTask, BaseTaskConfig

from ..log import logger
from ..reporters import BasePipelineReporter
from ..status import PipelineTaskStatus


class RegistryError(Exception):
    pass


class TaskRegistry(object):
    def __init__(self):
        self.tasks: Dict[str, Type[BaseTask]] = {}

    def register(self, cls):
        task_id = self.get_task_id(cls.__module__, cls.__name__)

        if task_id in self.tasks:
            raise RegistryError(f"Multiple tasks named {task_id} have been registered.")

        logger.debug(f"registering task {task_id}")

        self.tasks[task_id] = cls

    def get_task_id(self, module, class_name):
        return "{}.{}".format(module, class_name)

    def reset(self):
        self.tasks = {}

    def get_task_class(self, task_id):
        if task_id in self.tasks.keys():
            return self.tasks[task_id]
        return None

    def load_task_from_id(
        self,
        task_id: str,
        config: Dict[str, Any],
        reporter: BasePipelineReporter,
    ):
        cls = self.get_task_class(task_id)

        if not cls:
            reporter.report_task(
                task_id=task_id,
                status=PipelineTaskStatus.CONFIG_ERROR,
                message=f"No task named {task_id} is registered",
            )
            return None

        try:
            return cls(config=config)
        except Exception as e:
            reporter.report_task(
                task_id=task_id, status=PipelineTaskStatus.CONFIG_ERROR, message=str(e)
            )
            return None


task_registry = TaskRegistry()
