import time

from wildcoeus.pipelines.base import Pipeline
from wildcoeus.pipelines.tasks import Task, TaskConfig


class TaskWaitConfigType(TaskConfig):
    wait: int


#
#
# class EchoInputType(BaseModel):
#     message: str
#
#
# class SaveMessageTask(Task):
#     title = "Echo message"
#     ConfigType = TaskWaitConfigType
#     InputType = EchoInputType
#
#     def run(self, pipeline_id: str, run_id: str, cleaned_data):
#         time.sleep(self.cleaned_config.wait)
#         ValueStore.store(
#             pipeline_id=pipeline_id,
#             run_id=run_id,
#             key="message",
#             value=cleaned_data.message,
#         )
#
#
# class EchoMessageTask(Task):
#     title = "Echo message from Store"
#     ConfigType = TaskWaitConfigType
#     InputType = EchoInputType
#
#     def run(self, pipeline_id: str, run_id: str, cleaned_data):
#         time.sleep(self.cleaned_config.wait)
#         message = ValueStore.get(
#             pipeline_id=pipeline_id,
#             run_id=run_id,
#             key="message",
#         )
#         print(message)

#
# class BasicPipeline(Pipeline):
#     save_message = SaveMessageTask(config={"wait": 2})
#     echo_message = EchoMessageTask(config={"wait": 4})
#
#     class Meta:
#         title = "Basic pipeline with 2 steps"


class TestTaskIterator(Task):
    ConfigType = TaskWaitConfigType

    def run(self, *args, **kwargs):
        time.sleep(self.cleaned_config.wait)
        return True

    @classmethod
    def get_iterator(cls):
        return range(0, 3)


class TestIteratorPipeline(Pipeline):
    first = TestTaskIterator(config={"wait": 2})

    @classmethod
    def get_iterator(cls):
        return range(0, 2)

    class Meta:
        title = "Pipeline with Iterator"
