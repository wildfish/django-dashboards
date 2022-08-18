class Registry(object):
    def __init__(self):
        # Register dashboard classes
        self.dashboards = {}

    def register(self, cls):
        self.dashboards[cls.__name__] = cls


registry = Registry()
