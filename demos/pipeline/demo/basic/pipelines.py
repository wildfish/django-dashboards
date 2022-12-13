import time

from pydantic import BaseModel

from wildcoeus.pipelines import Pipeline, Task, TaskConfig
from wildcoeus.pipelines.models import ValueStore
from wildcoeus.pipelines.registry import pipeline_registry


class EchoConfigType(TaskConfig):
    wait: int


class EchoInputType(BaseModel):
    message: str


class SaveMessageTask(Task):
    title = "Echo message"
    ConfigType = EchoConfigType
    InputType = EchoInputType

    def run(self, pipeline_id: str, run_id: str, cleaned_data):
        time.sleep(self.cleaned_config.wait)
        print("I am runnings :)")
        ValueStore.store(
            pipeline_id=pipeline_id,
            run_id=run_id,
            key="message",
            value=cleaned_data.message,
        )


class EchoMessageTask(Task):
    title = "Echo message from Store"
    ConfigType = EchoConfigType
    InputType = EchoInputType

    def run(self, pipeline_id: str, run_id: str, cleaned_data):
        print("I am running too :)")
        message = ValueStore.get(
            pipeline_id=pipeline_id,
            run_id=run_id,
            key="message",
        )
        print(message)


@pipeline_registry.register
class BasicPipeline(Pipeline):
    save_message = SaveMessageTask(config={"wait": 5})
    echo_message = EchoMessageTask(config={"wait": 5, "parents": ["save_message"]})

    class Meta:
        title = "Basic pipeline with 2 steps"
