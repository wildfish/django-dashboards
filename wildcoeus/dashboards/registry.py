from wildcoeus.registry.registry import Registry


class DashboardRegistry(Registry):
    def __init__(self):
        super().__init__("dashboards")

    def get_graphql_dashboards(self):
        return {
            item._meta.name: item
            for item in self.items
            if item._meta.include_in_graphql
        }


registry = DashboardRegistry()
