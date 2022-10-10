import sys
from typing import Optional

from pydantic import BaseModel

from datorum_pipelines import (
    BasePipeline,
    BaseTask,
    BaseTaskConfig,
    PipelineConfigEntry,
)

from datorum_pipelines.pipelines.registry import pipeline_registry


class EchoConfigType(BaseTaskConfig):
    message: str


class Echo(BaseTask):
    task_id = "echo-task"
    ConfigType = EchoConfigType
    cleaned_config: EchoConfigType

    def run(self, cleaned_data):
        print(self.cleaned_config.message)


@pipeline_registry.register
class BasicPipeline(BasePipeline):
    pipeline_id = "basic-pipeline"
    config = [
        PipelineConfigEntry(
            name="Echo",
            id="first",
            config={"label": "First Echo", "message": "First"},
        ),
        PipelineConfigEntry(
            name="Echo",
            id="second",
            config={
                "parents": ["First Echo"],
                "label": "Second Echo",
                "message": "Second",
            },
        ),
    ]
