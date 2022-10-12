import time

from pydantic import BaseModel

from datorum_pipelines import (
    BasePipeline,
    BaseTask,
    BaseTaskConfig,
    PipelineConfigEntry,
)
from datorum_pipelines.models import ValueStore
from datorum_pipelines.pipelines.registry import pipeline_registry


class EchoConfigType(BaseTaskConfig):
    wait: int


class EchoInputType(BaseModel):
    message: str


class SaveMessage(BaseTask):
    title = "Echo message"
    ConfigType = EchoConfigType
    InputType = EchoInputType

    def run(self, pipeline_id: str, run_id: str, cleaned_data):
        time.sleep(self.cleaned_config.wait)
        ValueStore.store(
            pipeline_id=pipeline_id,
            run_id=run_id,
            key="message",
            value=cleaned_data.message,
        )


class EchoMessage(BaseTask):
    title = "Echo message from Store"
    ConfigType = EchoConfigType
    InputType = EchoInputType

    def run(self, pipeline_id: str, run_id: str, cleaned_data):
        message = ValueStore.get(
            pipeline_id=pipeline_id,
            run_id=run_id,
            key="message",
        )
        print(message)


@pipeline_registry.register
class BasicPipeline(BasePipeline):
    title = "Basic pipline with 2 steps"
    config = [
        PipelineConfigEntry(id="first", task=SaveMessage, config={"wait": 5}),
        PipelineConfigEntry(
            id="second",
            task=EchoMessage,
            config={"parents": ["first"], "wait": 4},
        ),
    ]
    graph = {
        "second": {"first"},
    }  # todo: can parents use this instead?
