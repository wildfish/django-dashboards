from enum import Enum


class PipelineTaskStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    DONE = "DONE"
    CONFIG_ERROR = "CONFIG_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    RUNTIME_ERROR = "RUNTIME_ERROR"
    CANCELLED = "CANCELLED"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


FAILED_STATUES = [
    PipelineTaskStatus.CONFIG_ERROR.name,
    PipelineTaskStatus.VALIDATION_ERROR.name,
    PipelineTaskStatus.RUNTIME_ERROR.name,
    PipelineTaskStatus.CANCELLED.name,
]
