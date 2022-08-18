class Registry(object):
    def __init__(self):
        # Register dashboard classes
        self.dashboards = {}

    def register(self, cls):
        if (
            cls.__name__ != "Dashboard"
        ):  # TODO needs better way to exclude the base class?
            self.dashboards[cls.__name__] = cls

    def get_all_dashboards(self):
        return self.dashboards

    def get_graphql_dashboards(self):
        return {
            name: dashboard
            for name, dashboard in self.dashboards.items()
            if dashboard.include_in_graphql
        }


registry = Registry()