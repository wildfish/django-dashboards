import uuid
from typing import Callable

from django.core.management.base import BaseCommand

from wildcoeus.pipelines import config
from wildcoeus.pipelines.registry import pipeline_registry
from wildcoeus.pipelines.runners.celery.tasks import run_pipeline
from wildcoeus.pipelines.runners.eager import Runner as EagerRunner


class Command(BaseCommand):
    invalid = "Invalid input"

    def _handle_input(self, text: str, cast: Callable = str):
        try:
            return cast(input(f"\n{text}? "))
        except ValueError:
            self.stdout.write(self.invalid)
            exit()

    def handle(self, *args, **options):
        """
        Allow user to run a pipeline.
        """
        self.stdout.write("Pipelines:\n")
        pipeline_selection_key = {}
        for i, p in enumerate(pipeline_registry.get_all_registered_pipeline_ids(), 1):
            self.stdout.write(f"{i}). {p}:")
            pipeline_selection_key[i] = p

        selected_pipeline = self._handle_input(
            text="Which pipelines would you like to start", cast=int
        )

        if selected_pipeline not in pipeline_selection_key.keys():
            self.stdout.write("Invalid pipeline selected")
            exit()

        pipeline_id = pipeline_selection_key[selected_pipeline]
        pipeline_cls = pipeline_registry.get_pipeline_class(pipeline_id)

        self.stdout.write(f"{pipeline_id} will run the following tasks:\n")
        for i, (k, t) in enumerate(pipeline_cls.tasks.items(), 1):
            self.stdout.write(f"{i}). {k}: {t.title}")

        selected_action = self._handle_input(
            text="Run [r], Run eager [e] or Cancel [c]"
        )

        if selected_action not in ["r", "e", "c"]:
            self.stdout.write(self.invalid)
            exit()

        run_id = str(uuid.uuid4())
        input_data = {}  # TODO if there is any we'd need this as arg maybe?

        if selected_action == "c":
            exit()
        elif selected_action == "r":
            run_pipeline.delay(
                pipeline_id=pipeline_id, run_id=run_id, input_data=input_data
            )
            self.stdout.write("Pipeline scheduled in celery")
        else:
            reporter = config.Config().WILDCOEUS_DEFAULT_PIPELINE_REPORTER
            runner = EagerRunner()

            pipeline_cls().start(
                run_id=run_id,
                input_data=input_data,
                runner=runner,
                reporter=reporter,
            )

            self.stdout.write("Pipeline Completed")
