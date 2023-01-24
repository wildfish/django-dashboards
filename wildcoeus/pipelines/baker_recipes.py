from django.utils.timezone import make_aware

from faker import Faker
from model_bakery.recipe import Recipe, foreign_key, seq

from wildcoeus.pipelines.models import (
    PipelineExecution,
    PipelineLog,
    PipelineResult,
    TaskExecution,
    TaskResult,
)
from wildcoeus.pipelines.status import PipelineTaskStatus


fake = Faker()


fake_pipeline_execution = Recipe(
    PipelineExecution,
    pipeline_id=seq("tests.pipelines.fixtures.TestPipeline"),
    run_id=fake.uuid4,
    status=PipelineTaskStatus.PENDING.value,
    started=lambda: make_aware(fake.date_time_this_month()),
)


fake_pipeline_result = Recipe(
    PipelineResult,
    execution=foreign_key(fake_pipeline_execution),
    status=PipelineTaskStatus.PENDING.value,
    started=lambda: make_aware(fake.date_time_this_month()),
)


fake_task_execution = Recipe(
    TaskExecution,
    pipeline_result=foreign_key(fake_pipeline_result),
    pipeline_task="first",
    task_id=seq("tests.pipelines.fixtures.TaskFirst"),
    status=PipelineTaskStatus.PENDING.value,
    started=lambda: make_aware(fake.date_time_this_month()),
)


fake_task_result = Recipe(
    TaskResult,
    execution=foreign_key(fake_task_execution),
    status=PipelineTaskStatus.PENDING.value,
    started=lambda: make_aware(fake.date_time_this_month()),
    completed=lambda: make_aware(fake.date_time_this_month()),
)


fake_pipeline_log = Recipe(
    PipelineLog,
    pipeline_id="tests.pipelines.fixtures.TestPipeline",
    run_id=fake.uuid4,
    status=PipelineTaskStatus.PENDING.value,
    message="Done",
)
