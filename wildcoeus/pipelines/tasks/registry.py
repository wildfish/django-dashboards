from typing import Any, Dict

from wildcoeus.registry.registry import Registry


class TaskRegistry(Registry):
    def load_task_from_id(
        self,
        pipeline_task: str,
        task_id: str,
        config: Dict[str, Any],
    ):
        cls = self.get_by_id(task_id)

        task = cls(config=config)
        task.pipeline_task = pipeline_task

        return task


task_registry = TaskRegistry()
