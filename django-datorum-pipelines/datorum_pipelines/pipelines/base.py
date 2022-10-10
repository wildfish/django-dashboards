from typing import TYPE_CHECKING, Any, Dict, List, Optional, cast

from pydantic import BaseModel


if TYPE_CHECKING:  # pragma: nocover
    from ..runners import BasePipelineRunner

from ..reporters import BasePipelineReporter
from ..status import PipelineTaskStatus
from ..tasks import BaseTask, task_registry
from ..log import logger


class PipelineConfigEntry(BaseModel):
    name: str
    id: str
    config: Dict[str, Any]  # payload?


PipelineConfig = List[PipelineConfigEntry]


class BasePipeline:
    pipeline_id: str
    config: PipelineConfig

    def __init__(self):
        self.cleaned_tasks: List[Optional[BaseTask]] = []

    def clean_parents(
        self, task: BaseTask, all_tasks: List[BaseTask], reporter: BasePipelineReporter
    ):
        other_labels = list(
            map(
                lambda t: getattr(t.cleaned_config, "label", None),
                (
                    t
                    for t in all_tasks
                    if t
                    and t.id != task.id
                    and getattr(t.cleaned_config, "label", None)
                ),
            )
        )

        parent_labels = getattr(task.cleaned_config, "parents", []) or []
        if not all(p in other_labels for p in parent_labels):
            reporter.report_task(
                task.id,
                PipelineTaskStatus.CONFIG_ERROR,
                "One or more of the parent labels are not in the pipeline",
            )
            return None

        return task

    def clean_tasks(
        self, reporter: "BasePipelineReporter"
    ) -> List[Optional["BaseTask"]]:
        # load all the tasks from the config, if there are any errors they will be reported and None
        # will be stored for hte task
        tasks = list(
            map(
                lambda task_config: task_registry.load(
                    task_config.name, task_config.id, task_config.config, reporter
                ),
                self.config,
            )
        )

        # check that all tasks with parents have a task with the parent label present
        return list(
            map(
                lambda t: self.clean_parents(t, tasks, reporter) if t else t,
                tasks,
            )
        )

    def start(
        self,
        input_data: Dict[str, Any],
        runner: "BasePipelineRunner",
        reporter: "BasePipelineReporter",
    ) -> bool:
        reporter.report_pipeline(
            self.pipeline_id,
            PipelineTaskStatus.PENDING,
            "Pipeline is waiting to start",
        )

        self.cleaned_tasks = self.clean_tasks(reporter)

        if any(t is None for t in self.cleaned_tasks):
            # if any of the tasks have an invalid config cancel all others
            for task in (t for t in self.cleaned_tasks if t is not None):
                reporter.report_task(
                    task.id,
                    PipelineTaskStatus.CANCELLED,
                    "Tasks cancelled due to an error in the pipeline config",
                )
            return False
        else:
            cleaned_tasks = cast(List[BaseTask], self.cleaned_tasks)

            # else mark them all as pending
            for task in cleaned_tasks:
                reporter.report_task(
                    task.id,
                    PipelineTaskStatus.PENDING,
                    "Task is waiting to start",
                )

        return runner.start(self.pipeline_id, cleaned_tasks, input_data, reporter)
