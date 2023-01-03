from dataclasses import dataclass
from typing import Optional

from .forms import SearchForm
from .models import Repo
from wildcoeus.dashboards.component import Stat, Form
from wildcoeus.dashboards.dashboard import Dashboard
from wildcoeus.dashboards.registry import registry


def get_change_stat_data(prop, **kwargs):
    full_name = kwargs.get("filters", {}).get("full_name", None)
    obj = Repo.objects.filter(full_name=full_name.lower().strip()).first() if full_name else None

    if not obj or obj.latest_stats is None:
        return {
            "text": "-",
            "sub_text": "-",
            "full_name": full_name
        }

    latest = getattr(obj.latest_stats, prop)
    change = getattr(obj.latest_stats_change, prop)
    return {
        "text": latest,
        "sub_text": change if change is not None else "-",
        "full_name": full_name
    }


@dataclass
class SSEStat(Stat):
    template_name: str = "wildcoeus/dashboards/components/sse_stat.html"
    poll_rate: Optional[int] = 10

    @staticmethod
    def pushpin_url():
        """
        Assuming docker pushpin is running, in real world this would be proxied to application.
        """
        return "http://localhost:7999/events/"


@registry.register
class RepoDashboard(Dashboard):
    form = Form(form=SearchForm, dependents=["stars", "watchers", "open_issues", "forks"], method="post")
    stars = SSEStat(value=lambda *args, **kwargs: get_change_stat_data("stars_count", *args, **kwargs))
    watchers = SSEStat(value=lambda *args, **kwargs: get_change_stat_data("watchers_count", *args, **kwargs))
    open_issues = SSEStat(value=lambda *args, **kwargs: get_change_stat_data("open_issues_count", *args, **kwargs))
    forks = SSEStat(value=lambda *args, **kwargs: get_change_stat_data("forks_count", *args, **kwargs))

    class Meta:
        name = "Github Stats Fetcher"
        model = Repo
