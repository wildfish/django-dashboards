from typing import Any, Dict

from wildcoeus.registry.registry import Registry


class TaskRegistry(Registry):
    """
    Registry to contain all tasks within the project.
    """

    def load_task_from_id(
        self,
        pipeline_task: str,
        task_id: str,
        config: Dict[str, Any],
    ):
        """
        Fetches a task class from the registry and instantiates it with
        the provided config.

        :param pipeline_task: The property name the task is assigned to on the pipeline
        :param task_id: The id of the registered task class
        :param config: The config to create the task with
        """
        cls = self.get_by_id(task_id)

        task = cls(config=config)
        task.pipeline_task = pipeline_task

        return task


task_registry = TaskRegistry()
