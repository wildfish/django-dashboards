from graphlib import TopologicalSorter
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, cast

from django.utils import timezone

from pydantic import BaseModel


if TYPE_CHECKING:  # pragma: nocover
    from ..runners import BasePipelineRunner

from ..log import logger
from ..reporters import BasePipelineReporter
from ..status import PipelineTaskStatus
from ..tasks import BaseTask, task_registry
from .registry import pipeline_registry


class PipelineConfigEntry(BaseModel):
    task: Type[BaseTask]
    id: str
    config: Dict[str, Any]


PipelineConfig = List[PipelineConfigEntry]


class BasePipeline:
    title: str = ""
    config: PipelineConfig
    graph: Dict[str, Any]
    # todo: add these to control running on schedule(cron)? - copied from airflow
    # schedule_interval
    # start_date

    def __init__(self):
        self.slug = pipeline_registry.get_slug(self.__module__, self.__class__.__name__)
        self.cleaned_tasks: List[Optional[BaseTask]] = []

    def clean_parents(
        self,
        task_config: PipelineConfigEntry,
        all_task_configs: List[PipelineConfigEntry],
        reporter: BasePipelineReporter,
    ):
        # load task from registry
        task = task_registry.load_task_from_slug(
            task_registry.get_slug(
                task_config.task.__module__, task_config.task.__name__
            ),
            task_config,
            reporter,
        )

        # we cannot find task in registry
        if not task:
            return None

        other_ids = list(
            map(
                lambda c: c.id,
                (c for c in all_task_configs if c and c.id != task_config.id),
            )
        )

        parent_ids = getattr(task_config.config, "parents", []) or []

        logger.debug(f"id: {task_config.id}")
        logger.debug(f"other: {other_ids}")
        logger.debug(f"parents: {parent_ids}")
        if not all(p in other_ids for p in parent_ids):
            reporter.report_task(
                task.id,
                PipelineTaskStatus.CONFIG_ERROR,
                "One or more of the parent ids are not in the pipeline",
            )
            return None

        return task

    def clean_tasks(
        self, reporter: "BasePipelineReporter"
    ) -> List[Optional["BaseTask"]]:
        # check that all configs with parents have a task with the parent label present
        tasks = list(
            map(
                lambda c: self.clean_parents(c, self.config, reporter) if c else c,
                self.config,
            )
        )

        return tasks

    def start(
        self,
        run_id: str,
        input_data: Dict[str, Any],
        runner: "BasePipelineRunner",
        reporter: "BasePipelineReporter",
    ) -> bool:
        from ..models import PipelineExecution

        reporter.report_pipeline(
            self.slug,
            PipelineTaskStatus.PENDING,
            "Pipeline is waiting to start",
        )

        self.cleaned_tasks = self.clean_tasks(reporter)

        if any(t is None for t in self.cleaned_tasks):
            # if any of the tasks have an invalid config cancel all others
            for task in (t for t in self.cleaned_tasks if t is not None):
                reporter.report_task(
                    task.slug,
                    PipelineTaskStatus.CANCELLED,
                    "Tasks cancelled due to an error in the pipeline config",
                )
            return False
        else:
            cleaned_tasks = cast(List[BaseTask], self.cleaned_tasks)

            # else mark them all as pending
            for task in cleaned_tasks:
                reporter.report_task(
                    task.slug,
                    PipelineTaskStatus.PENDING,
                    "Task is waiting to start",
                )

        started = runner.start(self.slug, run_id, cleaned_tasks, input_data, reporter)
        # record when it started
        if started:
            PipelineExecution.objects.update_or_create(
                pipeline_id=self.slug, defaults={"last_run": timezone.now()}
            )

        return started

    @property
    def dag(self):
        ts = TopologicalSorter(self.graph)
        return tuple(ts.static_order())
