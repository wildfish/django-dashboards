from django.template.loader import render_to_string

import requests
from django_eventstream import send_event
from pydantic import BaseModel

from wildcoeus.dashboards.component import Stat
from wildcoeus.pipelines import Pipeline, Task
from wildcoeus.pipelines.registry import pipeline_registry

from .models import Repo, RepoStats, RepoStatsChange


def build_event(key, value, change=None):
    stat = Stat(value={"text": value, "sub_text": change or "-"}, key=key)

    return render_to_string(
        stat.template_name,
        {
            "component": stat,
            "rendered_value": stat.get_value(),
        },
    )


class RepoTaskInput(BaseModel):
    full_name: str


class CalcRepoStatsChanges(Task):
    title = "Calculates the stats changes for a repo"
    InputType = RepoTaskInput

    def run(self, pipeline_id: str, run_id: str, cleaned_data: RepoTaskInput):
        late, early = RepoStats.objects.filter(
            repo__full_name=cleaned_data.full_name
        ).order_by("-updated_at")[:2]

        change = RepoStatsChange.objects.create(
            repo=late.repo,
            late_stats=late,
            early_stats=early,
            stars_count=late.stars_count - early.stars_count,
            watchers_count=late.watchers_count - early.watchers_count,
            forks_count=late.forks_count - early.forks_count,
            open_issues_count=late.open_issues_count - early.open_issues_count,
        )

        send_event(
            "test",
            f"repos-{cleaned_data.full_name}-stars",
            build_event("stars", late.stars_count, change.stars_count),
            json_encode=False,
        )
        send_event(
            "test",
            f"repos-{cleaned_data.full_name}-forks",
            build_event("forks", late.forks_count, change.forks_count),
            json_encode=False,
        )
        send_event(
            "test",
            f"repos-{cleaned_data.full_name}-watchers",
            build_event("watchers", late.watchers_count, change.watchers_count),
            json_encode=False,
        )
        send_event(
            "test",
            f"repos-{cleaned_data.full_name}-open_issues",
            build_event(
                "open_issues", late.open_issues_count, change.open_issues_count
            ),
            json_encode=False,
        )


class FetchLatestRepoStats(Task):
    title = "Collects the latest stats on the repo"
    InputType = RepoTaskInput

    def run(self, pipeline_id: str, run_id: str, cleaned_data: RepoTaskInput):
        res = requests.get(f"https://api.github.com/repos/{cleaned_data.full_name}")

        if res.status_code < 200 or res.status_code >= 400:
            send_event(
                f"repos-{cleaned_data.full_name}",
                "message",
                {"error": res.text, "status": res.status_code},
            )
            raise Exception(f"Bad response from github: {res.status_code} - {res.text}")

        data = res.json()

        repo = Repo.objects.get_or_create(
            full_name=data.get("full_name"),
            defaults={
                "name": data.get("name"),
                "gh_id": data.get("id"),
            },
        )[0]

        stat = RepoStats.objects.create(
            repo=repo,
            gh_url=data.get("url"),
            homepage=data.get("homepage", ""),
            description=data.get("description", ""),
            language=data.get("language", ""),
            gh_created_at=data.get("created_at"),
            gh_updated_at=data.get("updated_at"),
            gh_pushed_at=data.get("pushed_at"),
            stars_count=data.get("stargazers_count"),
            watchers_count=data.get("watchers_count"),
            forks_count=data.get("forks_count"),
            open_issues_count=data.get("open_issues_count"),
        )

        send_event(
            "test",
            f"repos-{cleaned_data.full_name}-stars",
            build_event("stars", stat.stars_count),
            json_encode=False,
        )
        send_event(
            "test",
            f"repos-{cleaned_data.full_name}-forks",
            build_event("forks", stat.forks_count),
            json_encode=False,
        )
        send_event(
            "test",
            f"repos-{cleaned_data.full_name}-watchers",
            build_event("watchers", stat.watchers_count),
            json_encode=False,
        )
        send_event(
            "test",
            f"repos-{cleaned_data.full_name}-open_issues",
            build_event("open_issues", stat.open_issues_count),
            json_encode=False,
        )


@pipeline_registry.register
class UpdateRepoStats(Pipeline):
    fetch_latest = FetchLatestRepoStats()
    calc_changes = CalcRepoStatsChanges()

    class Meta:
        title = "Fetches repo stats and calculates the any changes"
