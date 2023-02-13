from unittest import mock
from unittest.mock import Mock, call

import pytest

from wildcoeus.pipelines.base import Pipeline
from wildcoeus.pipelines.models import OrmTaskResult
from wildcoeus.pipelines.registry import pipeline_registry
from wildcoeus.pipelines.runners.eager import Runner
from wildcoeus.pipelines.status import PipelineTaskStatus
from wildcoeus.pipelines.tasks.base import Task


pytestmark = pytest.mark.django_db()


def test_task_have_no_parents___tasks_are_ran_in_configured_order():
    reporter = Mock()

    class TestTask(Task):
        class Meta:
            app_label = "pipelinetest"

        def run(self, *args, **kwargs):
            return True

    class TestTaskTwo(Task):
        class Meta:
            app_label = "pipelinetest"

        def run(self, *args, **kwargs):
            return True

    class TestPipeline(Pipeline):
        first = TestTask(config={})
        second = TestTaskTwo(config={})

        class Meta:
            app_label = "pipelinetest"

    pipeline = TestPipeline()

    pipeline.start(run_id="123", input_data={}, runner=Runner(), reporter=reporter)

    first_task_result = OrmTaskResult.objects.filter(
        execution__pipeline_task="first"
    ).first()
    second_task_result = OrmTaskResult.objects.filter(
        execution__pipeline_task="second"
    ).first()

    assert reporter.report_context_object.call_args_list.index(
        call(
            first_task_result,
            PipelineTaskStatus.DONE,
            mock.ANY,
        )
    ) < reporter.report_context_object.call_args_list.index(
        call(
            second_task_result,
            PipelineTaskStatus.RUNNING,
            mock.ANY,
        )
    )


def test_task_with_parent_waits_for_parents_to_be_ran():
    reporter = Mock()

    class TestTask(Task):
        class Meta:
            app_label = "pipelinetest"

        def run(self, *args, **kwargs):
            return True

    class TestTaskTwo(Task):
        class Meta:
            app_label = "pipelinetest"

        def run(self, *args, **kwargs):
            return True

    class TestPipeline(Pipeline):
        child = TestTaskTwo(config={"parents": ["parent"]})
        parent = TestTask(config={})

        class Meta:
            app_label = "pipelinetest"

    pipeline = TestPipeline()

    pipeline.start(run_id="123", input_data={}, runner=Runner(), reporter=reporter)

    parent = OrmTaskResult.objects.filter(execution__pipeline_task="parent").first()
    child = OrmTaskResult.objects.filter(execution__pipeline_task="child").first()

    assert reporter.report_context_object.call_args_list.index(
        call(
            parent,
            PipelineTaskStatus.DONE,
            mock.ANY,
        )
    ) < reporter.report_context_object.call_args_list.index(
        call(
            child,
            PipelineTaskStatus.RUNNING,
            mock.ANY,
        )
    )


def test_first_task_fails___other_tasks_are_cancelled():
    reporter = Mock()

    class BadTask(Task):
        class Meta:
            app_label = "pipelinetest"

        def run(self, *args, **kwargs):
            raise Exception("Test error")

    good_task_start = Mock()

    class GoodTask(Task):
        class Meta:
            app_label = "pipelinetest"

        def start(self, *args, **kwargs):
            good_task_start(*args, **kwargs)

    class TestPipeline(Pipeline):
        bad = BadTask(config={})
        good = GoodTask(config={})

        class Meta:
            app_label = "pipelinetest"

    pipeline = TestPipeline()

    pipeline.start(run_id="123", input_data={}, runner=Runner(), reporter=reporter)

    bad = OrmTaskResult.objects.filter(execution__pipeline_task="bad").first()
    good = OrmTaskResult.objects.filter(execution__pipeline_task="good").first()

    assert reporter.report_context_object.call_args_list.index(
        call(
            bad,
            PipelineTaskStatus.RUNTIME_ERROR,
            mock.ANY,
        )
    ) < reporter.report_context_object.call_args_list.index(
        call(
            good,
            PipelineTaskStatus.CANCELLED,
            mock.ANY,
        )
    )

    good_task_start.assert_not_called()
