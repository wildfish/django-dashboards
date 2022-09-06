from typing import TYPE_CHECKING, Any, Dict, List, Optional

from pydantic import BaseModel


if TYPE_CHECKING:  # pragma: nocover
    from ..runners import BasePipelineRunner

from ..reporters import BasePipelineReporter, PipelineTaskStatus
from ..tasks import BaseTask, task_registry


class PipelineConfigEntry(BaseModel):
    name: str
    id: str
    config: Dict[str, Any]


PipelineConfig = List[PipelineConfigEntry]


class BasePipeline:
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.cleaned_tasks: Optional[List[BaseTask]] = None

    def clean_tasks(self, reporter: "BasePipelineReporter") -> List["BaseTask"]:
        return list(
            map(
                lambda task_config: task_registry.load(
                    task_config.name, task_config.id, task_config.config, reporter
                ),
                self.config,
            )
        )

    def start(
        self, runner: "BasePipelineRunner", reporter: "BasePipelineReporter"
    ) -> bool:
        self.cleaned_tasks = self.clean_tasks(reporter)

        if any(t is None for t in self.cleaned_tasks):
            # if any of the tasks have an invalid config cancel all others
            for task in filter(lambda t: t is not None, self.cleaned_tasks):
                reporter.report_task(
                    task.id,
                    PipelineTaskStatus.CANCELLED,
                    "Tasks cancelled due to an error in the pipeline config",
                )
            return False
        else:
            # else mark them all as pending
            for task in self.cleaned_tasks:
                reporter.report_task(
                    task.id,
                    PipelineTaskStatus.PENDING,
                    "Task is waiting to start",
                )

        return runner.start(self.cleaned_tasks)
