from django.contrib.humanize.templatetags.humanize import intcomma

from datorum.component import Chart, Map, Stat, Table, Text
from datorum.component.layout import HTML, Card, ComponentLayout
from datorum.component.text import StatData
from datorum.dashboard import Dashboard
from datorum.registry import registry

from demo.churn.data import ChurnSummaryData


class SummaryDashboard(Dashboard):
    number_risky_customers = Stat(
        value=StatData(text="2", sub_text="# Risky customers")
    )
    monthly_gross_margin = Stat(
        value=StatData(text=f"£{intcomma(12345678)}", sub_text="Monthly Gross Margin")
    )
    actual_churn_rate = Stat(value=StatData(text="1.6%", sub_text="Rate"))

    actual_churn_data = Text(value="actual_churn_data")
    churn_risk_predictor = Chart(defer=ChurnSummaryData.fetch_churn_risk_predictor)
    churn_by_geography = Map(defer=ChurnSummaryData.fetch_churn_by_geography)

    forecast_analysis = Chart(defer=ChurnSummaryData.fetch_churn_risk_predictor)
    churn_factors = Chart(defer=ChurnSummaryData.fetch_churn_risk_predictor)

    churn_table = Table(defer=ChurnSummaryData.fetch_churn_table)

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
            Card("actual_churn_data", width=4),
            Card("churn_risk_predictor", width=4),
            Card("churn_by_geography", width=4),
            Card("forecast_analysis", width=6),
            Card("churn_factors", width=6),
            Card("churn_table", width=12),
        )

    class Meta:
        name = "Summary"


registry.register(SummaryDashboard)
