from django.contrib.auth.models import User

import pytest

from wildcoeus.pipelines import Pipeline, Task
from wildcoeus.pipelines.base import ModelPipeline


@pytest.fixture
def test_task():
    class TestTask(Task):
        def run(self, *args, **kwargs):
            return True

    return TestTask


@pytest.fixture
def test_pipeline(test_task):
    class TestPipeline(Pipeline):
        first = test_task(config={})

        class Meta:
            title = "Test Pipeline"

    return TestPipeline


@pytest.fixture
def test_model_pipeline(test_task):
    class TestPipeline(ModelPipeline):
        first = test_task(config={})

        class Meta:
            title = "Test Pipeline"
            model = User

    return TestPipeline


@pytest.fixture
def test_model_pipeline_qs(test_task):
    class TestPipeline(ModelPipeline):
        first = test_task(config={})

        class Meta:
            title = "Test Pipeline"
            queryset = User.objects.all()

    return TestPipeline