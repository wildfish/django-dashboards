from typing import Any, List, Type

from django.utils.module_loading import autodiscover_modules

from dashboards.log import logger


class Registrable:
    """
    Base class for any class that should be registered in a registry.
    """

    _meta: Any

    @classmethod
    def get_id(cls):
        """
        Returns an id for to be used in registration
        """
        raise NotImplementedError()

    @classmethod
    def get_urls(cls):
        """
        Builds a list of urls for the registrable object
        """
        return []


class Registry(object):
    """
    Bucket to store and retrieve registered classes
    """

    items: List[Type[Registrable]]

    def __init__(self, module_name=None):
        """
        :param module_name: The name of the module to search for within django apps
            when :code:`autodiscover` is called.
        """
        self.module_name = module_name
        self.items = []
        self.discovered = False

    def __contains__(self, item):
        return item.get_id() not in list(map(lambda d: d.get_id(), self.items))

    def reset(self):
        """
        Removes all items from the registry and flags it as not yet
        being discovered
        """
        self.items = []
        self.discovered = False

    def remove(self, item):
        """
        Removes the provided item from the registry

        :param item: The item to remove
        """
        if item.get_id() in list(map(lambda d: d.get_id(), self.items)):
            self.items.remove(item)

    def register(self, cls):
        """
        Adds the provided class to the registry

        :param cls: The class to add
        """
        if cls.get_id() not in list(map(lambda d: d.get_id(), self.items)):
            self.items.append(cls)
        else:
            logger.warn(f"{cls.get_id()} already registered")

        return cls

    def get_all_items(self):
        """
        Returns all the items in the registry
        """
        return self.items

    def get_by_classname(self, app_label: str, classname: str):
        """
        Gets an item from teh registry.

        :param app_label: The app label the registered item belongs to
        :param classname: The name of the class to fetch
        """
        for item in self.items:
            if str(item.__name__).lower() == classname.lower() and (
                app_label and item._meta.app_label == app_label
            ):
                return item
        raise IndexError

    def get_by_app_label(self, app_label: str):
        """
        Returns all registered elements filtered by the provided app label

        :param app_label: The app label to filter objects by
        """
        return [d for d in self.items if d._meta.app_label == app_label]

    def get_by_id(self, _id):
        """
        Gets a specific element from the registry
        """
        for item in self.items:
            if item.get_id() == _id:
                return item
        raise IndexError

    def get_urls(self):
        """
        Returns a list of all urls from registered classes
        """
        urlpatterns = []

        for item in self.get_all_items():
            urlpatterns += item.get_urls()

        return urlpatterns

    @property
    def urls(self):
        """
        A list of all urls from registered classes
        """
        return self.get_urls()

    def autodiscover(self):
        """
        Searches all installed apps for modules matching the :code:`model_name`
        so that classes can register themselves.
        """
        if self.discovered:
            return

        if self.module_name:
            autodiscover_modules(self.module_name)
            self.discovered = True


class DashboardRegistry(Registry):
    def __init__(self):
        super().__init__("dashboards")


registry = DashboardRegistry()
