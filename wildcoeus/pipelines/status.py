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

    @classmethod
    def final_statuses(cls):
        return [
            cls.RUNTIME_ERROR,
            cls.CONFIG_ERROR,
            cls.VALIDATION_ERROR,
            cls.CANCELLED,
            cls.DONE,
        ]

    @classmethod
    def non_final_statuses(cls):
        return [
            cls.PENDING,
            cls.RUNNING,
        ]

    def has_advanced(self, new_state: "PipelineTaskStatus"):
        if self in self.final_statuses():
            return False
        elif new_state in self.final_statuses():
            return True

        ordering = [PipelineTaskStatus.PENDING.value, PipelineTaskStatus.RUNNING.value]
        return ordering.index(self.value) < ordering.index(new_state.value)


FAILED_STATUES = [
    PipelineTaskStatus.CONFIG_ERROR.name,
    PipelineTaskStatus.VALIDATION_ERROR.name,
    PipelineTaskStatus.RUNTIME_ERROR.name,
    PipelineTaskStatus.CANCELLED.name,
]
