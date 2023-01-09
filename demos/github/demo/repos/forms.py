from django import forms

from wildcoeus.dashboards.forms import DashboardForm
from wildcoeus.pipelines.runners.celery.tasks import run_pipeline


class SearchForm(DashboardForm):
    full_name = forms.CharField()

    def save(self, **kwargs):
        run_pipeline.delay(
            pipeline_id="demo.repos.pipelines.UpdateRepoStats",
            input_data=self.cleaned_data,
        )