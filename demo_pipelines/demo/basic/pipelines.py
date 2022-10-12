import sys
import time
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
    wait: int


class EchoInputType(BaseModel):
    message: str


class Echo(BaseTask):
    title = "Echo message"
    ConfigType = EchoConfigType
    InputType = EchoInputType

    def run(self, cleaned_data):
        print(f"waiting {self.cleaned_config.wait} seconds before running")
        time.sleep(self.cleaned_config.wait)
        print(cleaned_data.message)


@pipeline_registry.register
class BasicPipeline(BasePipeline):
    title = "Basic pipline with 2 steps"
    config = [
        PipelineConfigEntry(
            id="first",
            task=Echo,
            config={"wait": 5}
        ),
        PipelineConfigEntry(
            id="second",
            task=Echo,
            config={
                "parents": ["first"],
                "wait": 4
            },
        ),
        PipelineConfigEntry(
            id="third",
            task=Echo,
            config={
                "parents": ["first"],
                "wait": 3
            },
        ),
        PipelineConfigEntry(
            id="fourth",
            task=Echo,
            config={
                "parents": ["first"],
                "wait": 2
            },
        ),
    ]
    graph = {"second": {"first", "third"}, "fourth": {"first"}, "third": {"fourth"}}  # todo: can parents use this instead?
