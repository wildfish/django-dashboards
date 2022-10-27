import time

from pydantic import BaseModel

from datorum.pipelines import BasePipeline, BaseTask, BaseTaskConfig
from datorum.pipelines.models import ValueStore
from datorum.pipelines.registry import pipeline_registry


class EchoConfigType(BaseTaskConfig):
    wait: int


class EchoInputType(BaseModel):
    message: str


class SaveMessageTask(BaseTask):
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


class EchoMessageTask(BaseTask):
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
    save_message = SaveMessageTask(config={"wait": 5})
    echo_message = EchoMessageTask(config={"wait": 5, "parents": ["save_message"]})

    class Meta:
        title = "Basic pipeline with 2 steps"
