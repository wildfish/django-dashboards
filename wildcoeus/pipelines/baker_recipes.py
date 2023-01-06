from django.utils.timezone import make_aware

from faker import Faker
from model_bakery.recipe import Recipe, seq

from wildcoeus.pipelines.models import (
    PipelineExecution,
    PipelineLog,
    TaskLog,
    TaskResult,
)
from wildcoeus.pipelines.status import PipelineTaskStatus


fake = Faker()


fake_pipeline_execution = Recipe(
    PipelineExecution,
    pipeline_id=seq("tests.pipelines.fixtures.TestPipeline"),
    run_id=fake.uuid4,
    status=PipelineTaskStatus.DONE.value,
    started=lambda: make_aware(fake.date_time_this_month()),
)

fake_task_result = Recipe(
    TaskResult,
    pipeline_id="tests.pipelines.fixtures.TestPipeline",
    pipeline_task="first",
    task_id=seq("tests.pipelines.fixtures.TaskFirst"),
    run_id=fake.uuid4,
    status=PipelineTaskStatus.DONE.value,
    started=lambda: make_aware(fake.date_time_this_month()),
    completed=lambda: make_aware(fake.date_time_this_month()),
)


fake_pipeline_log = Recipe(
    PipelineLog,
    pipeline_id="tests.pipelines.fixtures.TestPipeline",
    run_id=fake.uuid4,
    status=PipelineTaskStatus.DONE.value,
    message="Done",
)


fake_task_log = Recipe(
    TaskLog,
    pipeline_task="first",
    task_id="tests.pipelines.fixtures.TaskFirst",
    run_id=fake.uuid4,
    status=PipelineTaskStatus.DONE.value,
    message="Done",
)
