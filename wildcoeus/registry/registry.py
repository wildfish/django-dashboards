from typing import Any, List, Type

from django.utils.module_loading import autodiscover_modules

from wildcoeus.pipelines.log import logger


class Registerable:
    _meta: Any

    @classmethod
    def get_id(cls):
        raise NotImplementedError()

    @classmethod
    def get_urls(cls):
        raise NotImplementedError()


class Registry(object):
    items: List[Type[Registerable]]

    def __init__(self, module_name=None):
        self.module_name = module_name
        self.items = []

    def __contains__(self, item):
        return item.get_id() not in list(map(lambda d: d.get_id(), self.items))

    def reset(self):
        self.items = []

    def remove(self, item):
        if item.get_id() in list(map(lambda d: d.get_id(), self.items)):
            self.items.remove(item)

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

    def get_by_id(self, _id):
        for item in self.items:
            if item.get_id() == _id:
                return item
        raise IndexError

    def get_urls(self):
        urlpatterns = []

        for item in self.get_all_items():
            urlpatterns += item.get_urls()

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls()

    def autodiscover(self):
        if self.module_name:
            autodiscover_modules(self.module_name)


registry = Registry()
