from django.views.generic import TemplateView

from demo.demo_app.dashboards import DemoDashboardOne


class NormalView(TemplateView):
    template_name = "datorum/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dashboard"] = DemoDashboardOne()

        return context
