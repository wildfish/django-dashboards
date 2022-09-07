from typing import TYPE_CHECKING, Dict, Type


if TYPE_CHECKING:  # pragma: no cover
    from .base import BaseTask

from ..reporters import BasePipelineReporter
from ..status import PipelineTaskStatus


class RegistryError(Exception):
    pass


class TaskRegistry(object):
    def __init__(self):
        self.tasks: Dict[str, Type[BaseTask]] = {}

    def register(self, cls):
        task_name = cls.name or cls.__name__

        if task_name in self.tasks:
            raise RegistryError(
                f"Multiple tasks named {task_name} have been registered."
            )

        self.tasks[task_name] = cls

    def reset(self):
        self.tasks = {}

    def load(self, name, task_id, config, reporter: BasePipelineReporter):
        cls = self.tasks.get(name)

        if not cls:
            reporter.report_task(
                task_id,
                PipelineTaskStatus.CONFIG_ERROR,
                f"No task named {name} is registered",
            )
            return None

        try:
            return cls(task_id, config=config)
        except Exception as e:
            reporter.report_task(task_id, PipelineTaskStatus.CONFIG_ERROR, str(e))
            return None


task_registry = TaskRegistry()
