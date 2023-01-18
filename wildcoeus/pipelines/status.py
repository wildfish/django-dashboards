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

    @property
    def final_statuses(self):
        return [self.RUNTIME_ERROR, self.CONFIG_ERROR, self.VALIDATION_ERROR, self.CANCELLED, self.DONE]

    def has_advanced(self, new_state: "PipelineTaskStatus"):
        if self in self.final_statuses:
            return False
        elif new_state in self.final_statuses:
            return True

        ordering = [self.PENDING, self.RUNNING]
        return ordering.index(self) < ordering.index(new_state)


FAILED_STATUES = [
    PipelineTaskStatus.CONFIG_ERROR.name,
    PipelineTaskStatus.VALIDATION_ERROR.name,
    PipelineTaskStatus.RUNTIME_ERROR.name,
    PipelineTaskStatus.CANCELLED.name,
]
