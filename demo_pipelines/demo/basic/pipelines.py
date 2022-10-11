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
    pass


class EchoInputType(BaseTaskConfig):
    message: str


class Echo(BaseTask):
    title = "Echo message"
    ConfigType = EchoConfigType
    InputType = EchoInputType

    def run(self, cleaned_data):
        print(cleaned_data.message)


@pipeline_registry.register
class BasicPipeline(BasePipeline):
    title = "Basic pipline with 2 steps"
    config = [
        PipelineConfigEntry(
            id="first",
            task=Echo,
            config={"message": "First"},
        ),
        PipelineConfigEntry(
            id="second",
            task=Echo,
            config={
                "parents": ["first"],
                "message": "Second",
            },
        ),
        PipelineConfigEntry(
            id="third",
            task=Echo,
            config={
                "parents": ["first"],
                "message": "Third",
            },
        ),
        PipelineConfigEntry(
            id="fourth",
            task=Echo,
            config={
                "parents": ["first"],
                "message": "Fourth",
            },
        ),
    ]
    graph = {"second": {"first", "third"}, "fourth": {"first"}, "third": {"fourth"}}  # todo: can parents use this instead?
