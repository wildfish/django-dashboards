from typing import Any, Dict, List

from .. import BasePipelineReporter
from ..tasks import BaseTask


class BasePipelineRunner:
    def start(
        self,
        pipeline_id: str,
        tasks: List[BaseTask],
        input_data: Dict[str, Any],
        reporter: BasePipelineReporter,
    ) -> bool:  # pragma: no cover
        pass
