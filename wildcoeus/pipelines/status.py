from enum import Enum


class PipelineTaskStatus(Enum):
    """
    The status of the task and pipeline statuses.
    """

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    DONE = "DONE"
    CONFIG_ERROR = "CONFIG_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    RUNTIME_ERROR = "RUNTIME_ERROR"
    CANCELLED = "CANCELLED"

    @classmethod
    def choices(cls):
        """
        Converts the enum into choices to be used in django models
        """
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def failed_statuses(cls):
        """
        Gets a list of statuses that represent a pipeline or tasks failing.
        """
        return [
            cls.RUNTIME_ERROR,
            cls.CONFIG_ERROR,
            cls.VALIDATION_ERROR,
            cls.CANCELLED,
        ]

    @classmethod
    def success_statuses(cls):
        """
        Gets a list of statuses that represent a pipeline or tasks succeeding.
        """
        return [
            cls.DONE,
        ]

    @classmethod
    def final_statuses(cls):
        """
        Gets a list of statuses that represent a pipeline or tasks finishing
        (whether successful or unsuccessful).
        """
        return [
            *cls.failed_statuses(),
            *cls.success_statuses(),
        ]

    @classmethod
    def non_final_statuses(cls):
        """
        Gets a list of statuses that represent a pipeline or tasks before
        finishing.
        """
        return [
            cls.PENDING,
            cls.RUNNING,
        ]

    def has_advanced(self, new_state: "PipelineTaskStatus"):
        """
        Checks if the provided status is later in the pipeline lifecycle.

        :param new_state: The state to check relative to ``self``
        """
        if self in self.final_statuses():
            return False
        elif new_state in self.final_statuses():
            return True

        ordering = [PipelineTaskStatus.PENDING.value, PipelineTaskStatus.RUNNING.value]
        return ordering.index(self.value) < ordering.index(new_state.value)
