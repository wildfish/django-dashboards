from typing import Any, Dict, Iterable, List

from ..celery_tasks import run_pipeline
from ..reporters import BasePipelineReporter
from ..status import PipelineTaskStatus
from ..tasks import BaseTask
from .base import BasePipelineRunner


class Runner(BasePipelineRunner):
    def start(
        self,
        pipeline_id: str,
        run_id: str,
        tasks: List[BaseTask],
        input_data: Dict[str, Any],
        reporter: BasePipelineReporter,
    ) -> bool:

        run_pipeline.delay(pipeline_id, run_id, input_data)

        return True
