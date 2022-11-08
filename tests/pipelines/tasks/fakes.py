from typing import Any, Dict, Optional
from unittest.mock import Mock

from pydantic import BaseModel

from wildcoeus.pipelines import BaseTask


def make_fake_task(input_type=None, config_type=None):
    class FakeTask(BaseTask):
        ConfigType = config_type or BaseTask.ConfigType
        InputType = input_type

        def __init__(
            self,
            config: Dict[str, Any] = None,
        ):
            super().__init__()
            self.input_data = None
            self.pipeline_task = "fake"
            self.run_body = Mock()

        def run(self, pipeline_id: str, run_id: str, cleaned_data: Optional[BaseModel]):
            self.run_body(cleaned_data)

    return FakeTask