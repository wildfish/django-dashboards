from django.urls import reverse_lazy

from datorum.component import CTA, Chart, Map, Stat, Table
from datorum.component.layout import HTML, Card, ComponentLayout
from datorum.component.text import CTAData, StatData
from datorum.dashboard import Dashboard
from datorum.registry import registry

from demo.churn.data import ChurnSummaryData


class SummaryDashboard(Dashboard):
    number_risky_customers = Stat(
        value=StatData(text="2", sub_text="# Risky customers")
    )

    monthly_gross_margin = Stat(value=ChurnSummaryData.fetch_monthly_gross_margin)
    actual_churn_rate = Stat(value=ChurnSummaryData.fetch_actual_churn_rate)

    actual_churn_data = Table(
        defer=ChurnSummaryData.fetch_actual_churn_data,
        columns=[
            {"data": "reference", "title": "Reference"},
            {"data": "product_cloud", "title": "Product Cloud"},
            {"data": "product_connectivity", "title": "Product Connectivity"},
            {"data": "product_licenses", "title": "Product Licenses"},
        ],
        page_size=10,
    )
    churn_by_geography = Map(defer=ChurnSummaryData.fetch_churn_by_geography)

    edit_scenarios = CTA(
        value=CTAData(
            href=reverse_lazy("churn:scenario_list"),
            text="Edit Scenarios",
        ),
    )
    forecast_analysis = Chart(defer=ChurnSummaryData.fetch_forecast_analysis)
    # churn_factors = Chart(defer=ChurnSummaryData.fetch_churn_risk_predictor)
    #
    churn_table = Table(
        defer=ChurnSummaryData.fetch_churn_table,
        columns=[
            {"data": "reference", "title": "Reference"},
            {"data": "name", "title": "Name"},
            {"data": "phone", "title": "Phone"},
            {"data": "email", "title": "Email"},
            {"data": "link_to_cms", "title": "CMS"},
        ],
        page_size=10,
    )

    class Layout(Dashboard.Layout):
        components = ComponentLayout(
            HTML(
                "This is the Churn Summary Dashboard Demo",
                width=12,
            ),
            "filter_form",
            Card("number_risky_customers", width=4),
            Card("monthly_gross_margin", width=4),
            Card("actual_churn_rate", width=4),
            Card("actual_churn_data", width=8),
            Card("churn_by_geography", width=4),
            Card("edit_scenarios", width=3),
            Card("forecast_analysis", width=9),
            # Card("forecast_analysis", width=6),
            # Card("churn_factors", width=6),
            Card("churn_table", width=12),
        )

    class Meta:
        name = "Summary"


class ForecastDashboard(Dashboard):
    forecast_analysis = Chart(defer=ChurnSummaryData.fetch_forecast_analysis)

    class Meta:
        name = "Forecast"


registry.register(SummaryDashboard)
registry.register(ForecastDashboard)
