from django.contrib.auth.models import User

import pytest

from tests.pipelines import pipelines


@pytest.fixture
def test_task():
    return pipelines.TestTask


@pytest.fixture
def test_task_iterator():
    return pipelines.TestTaskIterator


@pytest.fixture
def test_pipeline(test_task):
    return pipelines.TestPipeline


@pytest.fixture
def test_iterator_pipeline(test_task):
    return pipelines.TestIteratorPipeline


@pytest.fixture
def test_model_pipeline(test_task):
    return pipelines.TestModelPipeline


@pytest.fixture
def test_model_pipeline_qs(test_task):
    return pipelines.TestModelPipelineQS


@pytest.fixture
def user():
    user = User.objects.create(
        username="tester", is_active=True, email="tester@test.com"
    )
    user.set_password("password")
    user.save()
    return user


@pytest.fixture
def staff():
    user = User.objects.create(
        username="tester", is_active=True, email="tester@test.com", is_staff=True
    )
    user.set_password("password")
    user.save()
    return user
