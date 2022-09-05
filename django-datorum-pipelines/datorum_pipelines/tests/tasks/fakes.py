from typing import Any, Dict, Optional
from unittest.mock import Mock
from uuid import uuid4

from pydantic import BaseModel

from datorum_pipelines import BaseTask
from datorum_pipelines.reporter import BasePipelineReporter


def make_fake_task(input_type=None, config_type=None, task_name=None):
    class FakeTask(BaseTask):
        ConfigType = config_type
        InputType = input_type
        name = task_name or uuid4().hex

        def __init__(
            self,
            task_id: Optional[str] = None,
            reporter: Optional[BasePipelineReporter] = None,
            config: Optional[Dict[str, Any]] = None,
        ):
            super().__init__(task_id or uuid4().hex, reporter or Mock(), config=config)
            self.input_data = None
            self.run_body = Mock()

        def run(self, cleaned_data: Optional[BaseModel]):
            self.run_body(cleaned_data)

    return FakeTask
