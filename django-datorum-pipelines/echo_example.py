#!/usr/bin/env python
import logging
import sys
from typing import Optional

from pydantic import BaseModel

from datorum_pipelines import (
    BasePipeline,
    BaseTask,
    BaseTaskConfig,
    PipelineConfigEntry,
)
from datorum_pipelines.reporters.logging import LoggingReporter
from datorum_pipelines.runners.eager import EagerRunner


class EchoConfigType(BaseTaskConfig):
    message: str


class Echo(BaseTask):
    ConfigType = EchoConfigType
    cleaned_config: EchoConfigType

    def run(
        self,
        cleaned_data: Optional[BaseModel],
    ):
        logging.info(self.cleaned_config.message)


if __name__ == "__main__":
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    root.addHandler(handler)

    BasePipeline(
        "test-pipeline",
        [
            PipelineConfigEntry(
                name="Echo",
                id="first",
                config={"label": "First Echo", "message": "First"},
            ),
            PipelineConfigEntry(
                name="Echo",
                id="second",
                config={
                    "parents": ["First Echo"],
                    "label": "Second Echo",
                    "message": "Second",
                },
            ),
        ],
    ).start(
        {},
        EagerRunner(),
        LoggingReporter(),
    )
