from django.contrib.auth.models import User

from wildcoeus.pipelines import ModelPipeline, Pipeline, Task


class TestTask(Task):
    def run(self, *args, **kwargs):
        return True


class TestTaskIterator(Task):
    def run(self, *args, **kwargs):
        return True

    def get_iterator(self):
        return range(0, 3)


class TestPipeline(Pipeline):
    first = TestTask(config={})

    class Meta:
        title = "Test Pipeline"


class TestIteratorPipeline(Pipeline):
    first = TestTask(config={})

    def get_iterator(self):
        return range(0, 3)


class TestModelPipeline(ModelPipeline):
    first = TestTask(config={})

    class Meta:
        title = "Test Pipeline"
        model = User


class TestModelPipelineQS(ModelPipeline):
    first = TestTask(config={})

    class Meta:
        title = "Test Pipeline"

    def get_queryset(self, *args, **kwargs):
        return User.objects.all()
