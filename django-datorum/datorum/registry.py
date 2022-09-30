class Registry(object):
    def __init__(self):
        # Register dashboard classes
        self.dashboards = []

    def register(self, cls):
        self.dashboards.append(cls())

    def get_all_dashboards(self):
        return self.dashboards

    def get_by_classname(self, app_label: str, classname: str):
        for dashboard in self.dashboards:
            if dashboard.__class__.__name__ == classname and (
                app_label and dashboard.Meta.app_label == app_label
            ):
                return dashboard
        raise IndexError

    def get_by_slug(self, slug):
        for dashboard in self.dashboards:
            if dashboard.get_slug() == slug:
                return dashboard
        raise IndexError

    def get_graphql_dashboards(self):
        return {
            dashboard.Meta.name: dashboard
            for dashboard in self.dashboards
            if dashboard.include_in_graphql
        }

    def get_urls(self):
        urlpatterns = []

        for dashboard in self.get_all_dashboards():
            urlpatterns += dashboard.urls

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), "dashboards", "datorum"


registry = Registry()
