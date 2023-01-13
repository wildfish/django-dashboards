from typing import Any, Dict

from wildcoeus.pipelines.reporters import PipelineReporter
from wildcoeus.pipelines.status import PipelineTaskStatus
from wildcoeus.registry.registry import Registry


class TaskRegistry(Registry):
    def load_task_from_id(
        self,
        pipeline_task: str,
        task_id: str,
        run_id: str,
        config: Dict[str, Any],
        reporter: PipelineReporter,
    ):
        try:
            cls = self.get_by_id(task_id)

            task = cls(config=config)
            task.pipeline_task = pipeline_task

            return task
        except IndexError:
            reporter.report_task(
                pipeline_task=pipeline_task,
                task_id=task_id,
                run_id=run_id,
                status=PipelineTaskStatus.CONFIG_ERROR.value,
                message=f"No task named {task_id} is registered",
            )
            return None


task_registry = TaskRegistry()
