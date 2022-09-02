from typing import Any, Dict, Optional, Type

from pydantic import BaseModel, ValidationError

from ..reporter import BasePipelineReporter, PipelineTaskStatus


class TaskValidationError(Exception):
    pass


class BaseTask:
    InputType: Optional[Type[BaseModel]] = None

    def __init__(self, task_id: str, reporter: BasePipelineReporter):
        self.id = task_id
        self.reporter = reporter

    def clean_data(self, input_data: Optional[Dict[str, Any]]):
        if not input_data and self.InputType is not None:
            raise TaskValidationError("Input data was not provided when expected")

        if input_data and self.InputType is None:
            raise TaskValidationError("Input data was provided when not expected")

        if self.InputType is None:
            return {}

        try:
            model = self.InputType(**(input_data or {}))
            return model.dict()
        except ValidationError as e:
            raise TaskValidationError(e.json(indent=False))

    def start(self, input_data: Dict[str, Any]):
        try:
            cleaned_data = self.clean_data(input_data)
            self.run(cleaned_data)
        except TaskValidationError as e:
            self.reporter.report_task(
                self.id, PipelineTaskStatus.VALIDATION_ERROR, e.args[0]
            )

    def run(
        self,
        cleaned_data: Dict[str, Any],
    ):
        pass
