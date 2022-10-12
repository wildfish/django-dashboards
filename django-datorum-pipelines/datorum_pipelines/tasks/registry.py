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
        slug = self.get_slug(cls.__module__, cls.__name__)

        if slug in self.tasks:
            raise RegistryError(
                f"Multiple tasks named {task_name} have been registered."
            )

        logger.debug(f"registering task {slug}")

        self.tasks[slug] = cls

    def get_slug(self, module, class_name):
        return "{}.{}".format(module, class_name)

    def reset(self):
        self.tasks = {}

    def get_task_class(self, slug):
        if slug in self.tasks:
            return self.tasks[slug]
        return None

    def load_task_from_slug(
        self,
        slug: str,
        task_id: str,
        config: Dict[str, Any],
        reporter: BasePipelineReporter,
    ):
        cls = self.get_task_class(slug)

        if not cls:
            reporter.report_task(
                slug,
                PipelineTaskStatus.CONFIG_ERROR,
                f"No task named {slug} is registered",
            )
            return None

        try:
            return cls(task_id=task_id, config=config)
        except Exception as e:
            reporter.report_task(slug, PipelineTaskStatus.CONFIG_ERROR, str(e))
            return None


task_registry = TaskRegistry()
