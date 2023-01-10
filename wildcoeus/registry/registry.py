from typing import Sequence, Type

from wildcoeus.meta import ClassWithAppConfigMeta
from wildcoeus.pipelines.log import logger


class Registerable:
    _meta: Type[ClassWithAppConfigMeta.Meta]

    @classmethod
    def get_id(cls):
        raise NotImplementedError()


class Registry(object):
    items: Sequence[Type[Registerable]]

    def __init__(self):
        # Register item classes
        self.items = []

    def __contains__(self, item):
        return item.get_id() not in list(map(lambda d: d.get_id(), self.items))

    def reset(self):
        self.items = []

    def remove(self, cls):
        if cls.get_id() in list(map(lambda d: d.get_id(), self.items)):
            self.items.remove(cls)

    def register(self, cls):
        if cls.get_id() not in list(map(lambda d: d.get_id(), self.items)):
            self.items.append(cls)
        else:
            logger.warn(f"{cls.get_id()} already registered")

        return cls

    def get_all_items(self):
        return self.items

    def get_by_classname(self, app_label: str, classname: str):
        for item in self.items:
            if str(item.__name__).lower() == classname.lower() and (
                app_label and item._meta.app_label == app_label
            ):
                return item
        raise IndexError

    def get_by_app_label(self, app_label: str):
        return [d for d in self.items if d._meta.app_label == app_label]

    def get_by_slug(self, slug):
        for item in self.items:
            if item.get_id() == slug:
                return item
        raise IndexError

    def get_urls(self):
        urlpatterns = []

        for item in self.get_all_items():
            urlpatterns += item.urls()

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls()


registry = Registry()
