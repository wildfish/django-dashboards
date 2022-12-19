from django import template


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
