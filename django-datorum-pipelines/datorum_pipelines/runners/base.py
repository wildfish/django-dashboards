from typing import List

from ..tasks import BaseTask


class BasePipelineRunner:
    def start(self, tasks: List[BaseTask]) -> bool:  # pragma: no cover
        pass
