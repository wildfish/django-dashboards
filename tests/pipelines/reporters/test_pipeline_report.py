from unittest.mock import Mock

import pytest
from model_bakery import baker

from wildcoeus.pipelines.reporters import PipelineReporter
from wildcoeus.pipelines.status import PipelineTaskStatus


pytestmark = pytest.mark.django_db


class Reporter(PipelineReporter):
    def __init__(self):
        self.report_body = Mock()

    def report(self, *args, **kwargs):
        self.report_body(*args, **kwargs)


def pipeline_execution_factory():
    def fn():
        return "pipeline_execution", baker.make_recipe(
            "pipelines.fake_pipeline_execution",
            run_id="run_id",
            pipeline_id="pipeline_id",
        )

    return fn


def pipeline_result_factory(pipeline_object=None):
    def fn():
        pe = baker.make_recipe(
            "pipelines.fake_pipeline_execution",
            run_id="run_id",
            pipeline_id="pipeline_id",
        )
        return "pipeline_result", baker.make_recipe(
            "pipelines.fake_pipeline_result",
            execution=pe,
            serializable_pipeline_object=pipeline_object,
        )

    return fn


def task_execution_factory(pipeline_object=None):
    def fn():
        pe = baker.make_recipe(
            "pipelines.fake_pipeline_execution",
            run_id="run_id",
            pipeline_id="pipeline_id",
        )
        pr = baker.make_recipe(
            "pipelines.fake_pipeline_result",
            execution=pe,
            serializable_pipeline_object=pipeline_object,
        )
        return "task_execution", baker.make_recipe(
            "pipelines.fake_task_execution",
            task_id="task_id",
            pipeline_result=pr,
            pipeline_task="some_task",
        )

    return fn


def task_result_factory(pipeline_object=None, task_object=None):
    def fn():
        pe = baker.make_recipe(
            "pipelines.fake_pipeline_execution",
            run_id="run_id",
            pipeline_id="pipeline_id",
        )
        pr = baker.make_recipe(
            "pipelines.fake_pipeline_result",
            execution=pe,
            serializable_pipeline_object=pipeline_object,
        )
        te = baker.make_recipe(
            "pipelines.fake_task_execution",
            task_id="task_id",
            pipeline_task="some_task",
            pipeline_result=pr,
        )
        return "task_result", baker.make_recipe(
            "pipelines.fake_task_result",
            execution=te,
            serializable_task_object=task_object,
        )

    return fn


@pytest.mark.parametrize(
    ["factory", "message", "expected_message"],
    (
        (
            pipeline_execution_factory(),
            "",
            lambda o: f"Pipeline execution ({o.id}) pipeline_id: Pending",
        ),
        (
            pipeline_execution_factory(),
            "message",
            lambda o: f"Pipeline execution ({o.id}) pipeline_id: message",
        ),
        (
            pipeline_result_factory(),
            "",
            lambda o: f"Pipeline result ({o.id}) pipeline_id: Pending",
        ),
        (
            pipeline_result_factory(),
            "message",
            lambda o: f"Pipeline result ({o.id}) pipeline_id: message",
        ),
        (
            pipeline_result_factory(pipeline_object={"foo": "bar"}),
            "",
            lambda o: f"Pipeline result ({o.id}) pipeline_id: Pending | pipeline object:"
            + " {'foo': 'bar'}",
        ),
        (
            pipeline_result_factory(pipeline_object={"foo": "bar"}),
            "message",
            lambda o: f"Pipeline result ({o.id}) pipeline_id: message | pipeline object:"
            + " {'foo': 'bar'}",
        ),
        (
            task_execution_factory(),
            "",
            lambda o: f"Task execution ({o.id}) some_task (task_id): Pending",
        ),
        (
            task_execution_factory(),
            "message",
            lambda o: f"Task execution ({o.id}) some_task (task_id): message",
        ),
        (
            task_execution_factory(pipeline_object={"foo": "bar"}),
            "",
            lambda o: f"Task execution ({o.id}) some_task (task_id): Pending | pipeline object:"
            + " {'foo': 'bar'}",
        ),
        (
            task_execution_factory(pipeline_object={"foo": "bar"}),
            "message",
            lambda o: f"Task execution ({o.id}) some_task (task_id): message | pipeline object:"
            + " {'foo': 'bar'}",
        ),
        (
            task_result_factory(),
            "",
            lambda o: f"Task result ({o.id}) some_task (task_id): Pending",
        ),
        (
            task_result_factory(),
            "message",
            lambda o: f"Task result ({o.id}) some_task (task_id): message",
        ),
        (
            task_result_factory(task_object={"foo": "bar"}),
            "",
            lambda o: f"Task result ({o.id}) some_task (task_id): Pending | task object:"
            + " {'foo': 'bar'}",
        ),
        (
            task_result_factory(task_object={"foo": "bar"}),
            "message",
            lambda o: f"Task result ({o.id}) some_task (task_id): message | task object:"
            + " {'foo': 'bar'}",
        ),
        (
            task_result_factory(pipeline_object={"foo": "bar"}),
            "",
            lambda o: f"Task result ({o.id}) some_task (task_id): Pending | pipeline object:"
            + " {'foo': 'bar'}",
        ),
        (
            task_result_factory(pipeline_object={"foo": "bar"}),
            "message",
            lambda o: f"Task result ({o.id}) some_task (task_id): message | pipeline object:"
            + " {'foo': 'bar'}",
        ),
        (
            task_result_factory(
                pipeline_object={"foo": "bar"}, task_object={"boo": "far"}
            ),
            "",
            lambda o: f"Task result ({o.id}) some_task (task_id): Pending | pipeline object:"
            + " {'foo': 'bar'} | task object: {'boo': 'far'}",
        ),
        (
            task_result_factory(
                pipeline_object={"foo": "bar"}, task_object={"boo": "far"}
            ),
            "message",
            lambda o: f"Task result ({o.id}) some_task (task_id): message | pipeline object:"
            + " {'foo': 'bar'} | task object: {'boo': 'far'}",
        ),
    ),
)
def test_report(factory, message, expected_message):
    context_object_type, context_object = factory()

    reporter = Reporter()
    getattr(reporter, f"report_{context_object_type}")(
        context_object, PipelineTaskStatus.PENDING, message
    )

    reporter.report_body.assert_called_once_with(
        context_object,
        PipelineTaskStatus.PENDING,
        expected_message(context_object),
    )
