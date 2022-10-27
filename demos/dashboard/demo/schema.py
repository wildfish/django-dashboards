"""
    We'd probably want to do this differently I think, maybe a registry with an option like include_in_gql,
    which adds all dashboards automatically?

    We also have a little bit of a disjoint between URLs/views and dashboards.
    - URls/views help define the usage of dashboards multiple times
    - Urls>templates help select which layout to use
    - Title lives on the view.
    None of that might be an issue at this stage but need to have a think.
"""
import strawberry

from datorum.dashboards.schema import DashboardQuery


schema = strawberry.Schema(query=DashboardQuery)
