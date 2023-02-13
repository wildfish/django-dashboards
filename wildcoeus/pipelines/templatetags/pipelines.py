from datetime import datetime

from django import template
from django.utils.timezone import now

from wildcoeus.pipelines.status import PipelineTaskStatus


register = template.Library()


@register.filter(name="lookup")
def lookup(value, arg):
    return value.get(arg)


@register.filter
def duration(td):
    if not td:
        return None

    total_seconds = int(td.total_seconds())

    days = total_seconds // 86400
    remaining_hours = total_seconds % 86400
    remaining_minutes = remaining_hours % 3600
    hours = remaining_hours // 3600
    minutes = remaining_minutes // 60
    seconds = remaining_minutes % 60

    days_str = f"{days}d " if days else ""
    hours_str = f"{hours}h " if hours else ""
    minutes_str = f"{minutes}m " if minutes else ""
    seconds_str = f"{seconds}s" if seconds and not hours_str else ""

    return f"{days_str}{hours_str}{minutes_str}{seconds_str}"


@register.simple_tag
def status_class(status: str):
    return {
        PipelineTaskStatus.RUNNING.value: "result-primary",
        PipelineTaskStatus.DONE.value: "result-success",
        PipelineTaskStatus.CANCELLED.value: "result-cancelled",
        PipelineTaskStatus.PENDING.value: "result-pending",
        PipelineTaskStatus.RUNTIME_ERROR.value: "result-danger",
        PipelineTaskStatus.CONFIG_ERROR.value: "result-danger",
        PipelineTaskStatus.VALIDATION_ERROR.value: "result-danger",
    }[status]


@register.simple_tag
def status_text(status: str):
    return {
        PipelineTaskStatus.RUNNING.value: "Running",
        PipelineTaskStatus.DONE.value: "Done",
        PipelineTaskStatus.CANCELLED.value: "Cancelled",
        PipelineTaskStatus.PENDING.value: "Pending",
        PipelineTaskStatus.RUNTIME_ERROR.value: "Runtime Error",
        PipelineTaskStatus.CONFIG_ERROR.value: "Configuration Error",
        PipelineTaskStatus.VALIDATION_ERROR.value: "Input Validation Error",
    }[status]


@register.simple_tag
def duration_display(start: datetime | None, end: datetime | None):
    if not start:
        return "-"
    else:
        end = end or now()

        diff = end - start

        parts = [
            (int(diff.total_seconds() / 3600), "h"),
            (int(diff.total_seconds() / 60), "m"),
            (diff.seconds, "s"),
        ]

        return " ".join(f"{p[0]}{p[1]}" for p in parts if p[0])
