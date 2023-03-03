import logging
from unittest.mock import Mock

import pytest
from celery import chain, chord

from wildcoeus.pipelines.base import Pipeline
from wildcoeus.pipelines.registry import pipeline_registry
from wildcoeus.pipelines.results.helpers import build_pipeline_execution
from wildcoeus.pipelines.runners.celery.runner import Runner
from wildcoeus.pipelines.runners.celery.tasks import (
    run_pipeline_execution_report,
    run_pipeline_result_report,
    run_task,
    run_task_execution_report,
    run_task_result_report,
)
from wildcoeus.pipelines.status import PipelineTaskStatus
from wildcoeus.pipelines.tasks.base import Task


pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def celery_config():
    return {
        "broker_url": "memory://",
        "results_backend": "memory://",
        "task_always_eager": True,
    }


@pytest.fixture(autouse=True)
def logger(caplog):
    caplog.set_level(logging.INFO, logger="wildcoeus-pipelines")
    return caplog


def get_pipeline_execution(
    first_task_kwargs=None,
    second_task_kwargs=None,
    first_task_iterator=None,
    second_task_iterator=None,
    pipeline_iterator=None,
    pipeline_ordering=None,
):
    class First(Task):
        class Meta:
            app_label = "pipelinetest"

        def run(self, *args, **kwargs):
            return True

        @classmethod
        def get_iterator(cls):
            return first_task_iterator

    class Second(Task):
        class Meta:
            app_label = "pipelinetest"

        def run(self, *args, **kwargs):
            return True

        @classmethod
        def get_iterator(cls):
            return second_task_iterator

    @pipeline_registry.register
    class TestPipeline(Pipeline):
        first = First(**(first_task_kwargs or {}))
        second = Second(**(second_task_kwargs or {}))

        ordering = pipeline_ordering

        class Meta:
            app_label = "pipelinetest"

        @classmethod
        def get_iterator(cls):
            return pipeline_iterator

    return build_pipeline_execution(TestPipeline(), "run_id", Mock(), Mock(), {})


def test_build_celery_canvas___single_pipeline___canvas_is_chain():
    pipeline_execution = get_pipeline_execution()

    assert chain(
        Runner().expand_pipeline_result(pipeline_execution.get_pipeline_results()[0]),
        run_pipeline_execution_report.si(
            run_id=pipeline_execution.run_id,
            status=PipelineTaskStatus.DONE.value,
            message="Done",
        ),
    ) == Runner().expand_pipeline_execution(pipeline_execution)


def test_build_celery_canvas___multiple_pipeline___canvas_is_chord():
    pipeline_execution = get_pipeline_execution(pipeline_iterator=[1, 2])

    assert pipeline_execution.get_pipeline_results()[
        0
    ].serializable_pipeline_object == {"obj": 1}
    assert pipeline_execution.get_pipeline_results()[
        1
    ].serializable_pipeline_object == {"obj": 2}
    assert chord(
        [
            Runner().expand_pipeline_result(
                pipeline_execution.get_pipeline_results()[0]
            ),
            Runner().expand_pipeline_result(
                pipeline_execution.get_pipeline_results()[1]
            ),
        ],
        run_pipeline_execution_report.si(
            run_id=pipeline_execution.run_id,
            status=PipelineTaskStatus.DONE.value,
            message="Done",
        ),
    ) == Runner().expand_pipeline_execution(pipeline_execution)


def test_build_pipeline_chain___no_parents_set___tasks_are_added_in_defined_order():
    runner = Runner()
    pipeline_execution = get_pipeline_execution()
    pipeline_result = pipeline_execution.get_pipeline_results()[0]

    first_task_execution = next(
        e for e in pipeline_result.get_task_executions() if e.pipeline_task == "first"
    )
    second_task_execution = next(
        e for e in pipeline_result.get_task_executions() if e.pipeline_task == "second"
    )

    expected = chain(
        run_pipeline_result_report.si(
            pipeline_result_id=pipeline_result.id,
            status=PipelineTaskStatus.RUNNING.value,
            message="Running",
            propagate=True,
        ),
        runner.expand_celery_tasks(first_task_execution),
        runner.expand_celery_tasks(second_task_execution),
        run_pipeline_result_report.si(
            pipeline_result_id=pipeline_result.id,
            status=PipelineTaskStatus.DONE.value,
            message="Done",
            propagate=False,
        ),
    )
    expected.link_error(
        # Report pipeline error
        run_pipeline_result_report.si(
            pipeline_result_id=pipeline_result.id,
            status=PipelineTaskStatus.CANCELLED.value,
            message="Pipeline Error - remaining tasks cancelled",
            propagate=True,
        )
    )

    assert expected == Runner().expand_pipeline_result(pipeline_result)


def test_build_pipeline_chain___parents_swaps_order___tasks_are_added_respecting_parents():
    runner = Runner()

    pipeline_execution = get_pipeline_execution(pipeline_ordering={"first": ["second"]})
    pipeline_result = pipeline_execution.get_pipeline_results()[0]

    first_task_execution = next(
        e for e in pipeline_result.get_task_executions() if e.pipeline_task == "first"
    )
    second_task_execution = next(
        e for e in pipeline_result.get_task_executions() if e.pipeline_task == "second"
    )

    expected = chain(
        run_pipeline_result_report.si(
            pipeline_result_id=pipeline_result.id,
            status=PipelineTaskStatus.RUNNING.value,
            message="Running",
            propagate=True,
        ),
        runner.expand_celery_tasks(second_task_execution),
        runner.expand_celery_tasks(first_task_execution),
        run_pipeline_result_report.si(
            pipeline_result_id=pipeline_result.id,
            status=PipelineTaskStatus.DONE.value,
            message="Done",
            propagate=False,
        ),
    )
    expected.link_error(
        # Report pipeline error
        run_pipeline_result_report.si(
            pipeline_result_id=pipeline_result.id,
            status=PipelineTaskStatus.CANCELLED.value,
            message="Pipeline Error - remaining tasks cancelled",
            propagate=True,
        )
    )

    assert expected == Runner().expand_pipeline_result(pipeline_result)


def test_expand_celery_task___single_task___result_is_chain():
    runner = Runner()

    pipeline_execution = get_pipeline_execution()
    pipeline_result = pipeline_execution.get_pipeline_results()[0]

    first_task_execution = next(
        e for e in pipeline_result.get_task_executions() if e.pipeline_task == "first"
    )

    assert chain(
        runner.build_celery_task(first_task_execution.get_task_results()[0]),
        run_task_execution_report.si(
            task_execution_id=first_task_execution.id,
            status=PipelineTaskStatus.DONE.value,
            message="Done",
            propagate=False,
        ),
    ) == runner.expand_celery_tasks(first_task_execution)


def test_expand_celery_task___multiple_task___result_is_chord():
    runner = Runner()

    pipeline_execution = get_pipeline_execution(first_task_iterator=[1, 2])
    pipeline_result = pipeline_execution.get_pipeline_results()[0]

    first_task_execution = next(
        e for e in pipeline_result.get_task_executions() if e.pipeline_task == "first"
    )

    assert first_task_execution.get_task_results()[0].serializable_task_object == {
        "obj": 1
    }
    assert first_task_execution.get_task_results()[1].serializable_task_object == {
        "obj": 2
    }
    assert chord(
        [
            runner.build_celery_task(first_task_execution.get_task_results()[0]),
            runner.build_celery_task(first_task_execution.get_task_results()[1]),
        ],
        run_task_execution_report.si(
            task_execution_id=first_task_execution.id,
            status=PipelineTaskStatus.DONE.value,
            message="Done",
            propagate=False,
        ),
    ) == runner.expand_celery_tasks(first_task_execution)


def test_build_celery_task___no_queue_set___task_is_built_catching_errors_without_setting_a_queue():
    runner = Runner()

    pipeline_execution = get_pipeline_execution()
    pipeline_result = pipeline_execution.get_pipeline_results()[0]

    first_task_execution = next(
        e for e in pipeline_result.get_task_executions() if e.pipeline_task == "first"
    )
    first_task_result = first_task_execution.get_task_results()[0]

    expected = run_task.si(first_task_result.id)
    expected.link_error(
        run_task_result_report.si(
            task_result_id=first_task_result.id,
            status=PipelineTaskStatus.RUNTIME_ERROR.value,
            message="Task Error",
        )
    )
    expected.set(queue=None)

    assert expected == runner.build_celery_task(first_task_result)


def test_build_celery_task___queue_set___task_is_built_catching_errors_with_setting_a_queue():
    runner = Runner()

    pipeline_execution = get_pipeline_execution(
        first_task_kwargs={"config": {"celery_queue": "other"}}
    )
    pipeline_result = pipeline_execution.get_pipeline_results()[0]

    first_task_execution = next(
        e for e in pipeline_result.get_task_executions() if e.pipeline_task == "first"
    )
    first_task_result = first_task_execution.get_task_results()[0]

    expected = run_task.si(first_task_result.id)
    expected.link_error(
        run_task_result_report.si(
            task_result_id=first_task_result.id,
            status=PipelineTaskStatus.RUNTIME_ERROR.value,
            message="Task Error",
        )
    )
    expected.set(queue="other")

    assert expected == runner.build_celery_task(first_task_result)
