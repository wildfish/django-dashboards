from django.db.models import Avg
from django.db.models.functions import ExtractMonth, Round
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView

from demo.churn.dashboards import ForecastDashboard
from demo.churn.forms import ScenarioForm
from demo.churn.models import Customer, Scenario


class ScenarioListView(ListView):
    queryset = Scenario.objects.all().order_by("name")
    template_name = "demo/churn/scenario_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["averages"] = Customer.objects.average_values()
        context["forecast_dashboard"] = ForecastDashboard()
        return context


class ScenarioRowView(DetailView):
    model = Scenario
    template_name = "demo/churn/scenario_row.html"


class ScenarioEditView(UpdateView):
    form_class = ScenarioForm
    model = Scenario
    template_name = "demo/churn/scenario_edit.html"

    def get_success_url(self):
        return reverse("churn:scenario_row", kwargs={"pk": self.object.pk})
