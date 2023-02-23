from datetime import datetime, timedelta
from typing import Optional, List

from django import template
from django.utils.timezone import now

from wildcoeus.pipelines.status import PipelineTaskStatus


register = template.Library()


@register.filter(name="lookup")
def lookup(value, key):
    """
    Fetches the value for the provided key from a dict like structure.

    :param value: The object to lookup a value from
    :param key: The key of the value to lookup
    """
    return value.get(key)


@register.filter
def duration(delta_or_start: Optional[timedelta | datetime], end: Optional[datetime] = None):
    """
    Converts a time delta into a formatted string.

    The total number of seconds is used to decide how many parts the
    string should be broken down into.

    For example, the string may look like:

    * 35s (35 seconds)
    * 3m 2s (3 minutes and 2 seconds)
    * 1d 9h (1 day and 9 hours exactly)

    Returns :code:`None` if :code:`delta_or_start` is :code:`None`

    If :code:`delta_or_start` is a :code:`timedelta` object it will be used
    to generate the duration string.

    If :code:`delta_or_start` is a :code:`datetime` object it will be with
    :code:`end` to calculate a :code:`timedelta` object. If :code:`end`
    is :code:`None`, :code:`now` is used.

    :param delta_or_start: The timedelta to format or the start time for
        the duration
    :param end: The end time of the duration
    """
    if not delta_or_start:
        return None

    if isinstance(delta_or_start, datetime):
        end = end or now()
        diff = end - delta_or_start
    else:
        diff = delta_or_start

    total_seconds = int(diff.total_seconds())

    days = total_seconds // 86400
    remaining_hours = total_seconds % 86400
    remaining_minutes = remaining_hours % 3600
    hours = remaining_hours // 3600
    minutes = remaining_minutes // 60
    seconds = remaining_minutes % 60

    parts: List[str] = []
    if days:
        parts.append(f"{days}d")

    if hours:
        parts.append(f"{hours}h")

    if minutes:
        parts.append(f"{minutes}m")

    if seconds:
        parts.append(f"{seconds}s")

    return " ".join(parts)


@register.simple_tag
def status_class(status: str | PipelineTaskStatus):
    """
    Converts a pipeline status to a css class.

    :param status: Either a :code:`PipelineTaskStats` or its string
        representation to convert
    """
    if isinstance(status, PipelineTaskStatus):
        status = status.value

    return {
        PipelineTaskStatus.RUNNING.value: "result-primary",
        PipelineTaskStatus.DONE.value: "result-success",
        PipelineTaskStatus.CANCELLED.value: "result-cancelled",
        PipelineTaskStatus.PENDING.value: "result-pending",
        PipelineTaskStatus.RUNTIME_ERROR.value: "result-danger",
        PipelineTaskStatus.CONFIG_ERROR.value: "result-danger",
        PipelineTaskStatus.VALIDATION_ERROR.value: "result-danger",
    }.get(status, "")


@register.simple_tag
def status_text(status: str | PipelineTaskStatus):
    """
    Converts a pipeline status to a human friendly string.

    :param status: Either a :code:`PipelineTaskStats` or its string
        representation to convert
    """
    if isinstance(status, PipelineTaskStatus):
        status = status.value

    return {
        PipelineTaskStatus.RUNNING.value: "Running",
        PipelineTaskStatus.DONE.value: "Done",
        PipelineTaskStatus.CANCELLED.value: "Cancelled",
        PipelineTaskStatus.PENDING.value: "Pending",
        PipelineTaskStatus.RUNTIME_ERROR.value: "Runtime Error",
        PipelineTaskStatus.CONFIG_ERROR.value: "Configuration Error",
        PipelineTaskStatus.VALIDATION_ERROR.value: "Input Validation Error",
    }.get(status, "")

