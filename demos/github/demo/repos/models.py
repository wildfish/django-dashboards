from django.db import models
from django.utils.functional import cached_property


class Repo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, unique=True)
    gh_id = models.BigIntegerField()

    def __str__(self):
        return self.full_name

    @cached_property
    def latest_stats(self):
        return self.stats.order_by("-updated_at").first()

    @cached_property
    def latest_stats_change(self):
        return self.stats_change.order_by("-updated_at").first()


class RepoStats(models.Model):
    repo = models.ForeignKey(Repo, related_name="stats", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    gh_url = models.URLField()
    homepage = models.URLField(blank=True)
    description = models.TextField(default="", blank=True)
    language = models.CharField(max_length=255)

    gh_created_at = models.DateTimeField()
    gh_updated_at = models.DateTimeField()
    gh_pushed_at = models.DateTimeField()

    stars_count = models.BigIntegerField(default=None, null=True)
    watchers_count = models.BigIntegerField(default=None, null=True)
    forks_count = models.BigIntegerField(default=None, null=True)
    open_issues_count = models.BigIntegerField(default=None, null=True)


class RepoStatsChange(models.Model):
    repo = models.ForeignKey(
        Repo, related_name="stats_change", on_delete=models.CASCADE
    )
    early_stats = models.ForeignKey(
        RepoStats, related_name="early_change", on_delete=models.CASCADE
    )
    late_stats = models.ForeignKey(
        RepoStats, related_name="late_change", on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    stars_count = models.BigIntegerField(default=None, null=True)
    watchers_count = models.BigIntegerField(default=None, null=True)
    forks_count = models.BigIntegerField(default=None, null=True)
    open_issues_count = models.BigIntegerField(default=None, null=True)
