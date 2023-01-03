from wildcoeus.pipelines.log import logger


class Registry(object):
    def __init__(self):
        # Register dashboard classes
        self.dashboards = []

    def __contains__(self, item):
        item.get_slug() not in list(map(lambda d: d.get_slug(), self.dashboards))

    def reset(self):
        self.dashboards = []

    def remove(self, cls):
        if cls.get_slug() in list(map(lambda d: d.get_slug(), self.dashboards)):
            self.dashboards.remove(cls)

    def register(self, cls):
        if cls.get_slug() not in list(map(lambda d: d.get_slug(), self.dashboards)):
            self.dashboards.append(cls)
        else:
            logger.warn(f"{cls.get_slug()} already registered")

        return cls

    def get_all_dashboards(self):
        return self.dashboards

    def get_by_classname(self, app_label: str, classname: str):
        for dashboard in self.dashboards:
            if dashboard.class_name() == classname and (
                app_label and dashboard.Meta.app_label == app_label
            ):
                return dashboard
        raise IndexError

    def get_by_app_label(self, app_label: str):
        return [d for d in self.dashboards if d._meta.app_label == app_label]

    def get_by_slug(self, slug):
        for dashboard in self.dashboards:
            if dashboard.get_slug() == slug:
                return dashboard
        raise IndexError

    def get_graphql_dashboards(self):
        return {
            dashboard.Meta.name: dashboard
            for dashboard in self.dashboards
            if dashboard.Meta.include_in_graphql
        }

    def get_urls(self):
        urlpatterns = []

        for dashboard in self.get_all_dashboards():
            urlpatterns += dashboard.urls()

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls()


registry = Registry()
