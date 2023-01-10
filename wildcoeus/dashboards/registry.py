from typing import Sequence, Type

from wildcoeus.dashboards.dashboard import Dashboard
from wildcoeus.registry.registry import Registry


class DashboardRegistry(Registry):
    items: Sequence[Type[Dashboard]]

    def get_graphql_dashboards(self):
        return {
            item._meta.name: item
            for item in self.items
            if item._meta.include_in_graphql
        }


registry = DashboardRegistry()
