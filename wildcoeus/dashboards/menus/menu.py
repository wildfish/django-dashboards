from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Type, Union

from django.urls import resolve

from wildcoeus.dashboards.dashboard import Dashboard, ModelDashboard
from wildcoeus.dashboards.registry import registry
from wildcoeus.registry.registry import Registrable


def make_dashboard_item(
    d: Union[Type[Dashboard], Type[ModelDashboard]],
    obj: Optional[Any] = None,
    title: Optional[str] = None,
    children: Optional[List[Union["MenuItem", "DashboardMenuItem"]]] = None,
) -> "DashboardMenuItem":
    title = title if title else d._meta.name.split("-")[0]  # shorten name in menu

    if obj and issubclass(d, ModelDashboard):
        dashboard = d(object=obj)
        url = dashboard.get_absolute_url()
    else:
        # TODO: for some reason mypy complains about this one line
        url = d.get_absolute_url()  # type: ignore

    return DashboardMenuItem(
        title=title,
        url=url,
        dashboard=d,
        children=children,
    )


class Menu(Registrable):
    name: str

    @classmethod
    def get_id(cls) -> str:
        return cls.__name__

    @classmethod
    def render(
        cls, request, obj: Optional[Any] = None
    ) -> List[Union["MenuItem", "DashboardMenuItem"]]:
        available_items = []
        for item in cls.get_items(obj):
            item.render(request)
            if item.visible:
                available_items.append(item)

        return available_items

    @classmethod
    def get_items(
        cls, obj: Optional[Any] = None
    ) -> List[Union["MenuItem", "DashboardMenuItem"]]:
        raise NotImplementedError


class DashboardMenu(Menu):
    app_label: str

    @classmethod
    def get_items(cls, obj: Optional[Any] = None):
        """
        Get all the other urls for this section/app.

        If the machine is set, get the machine specific dashboards, to do this we need to init the
        dashboard and set the object manually.
        """
        urls = []

        for d in registry.get_by_app_label(cls.app_label):
            # only include if specified in dashboard meta
            if d._meta.include_in_menu:
                # is this is a ModelDashboard
                if issubclass(d, ModelDashboard):
                    # only include if we have an obj and is it the expected type
                    if obj and isinstance(obj, d._meta.model):
                        # # for model dashboards we need the dashboard instance
                        urls.append(make_dashboard_item(d, obj))
                else:
                    urls.append(make_dashboard_item(d))

        return urls


@dataclass(kw_only=True)
class MenuItem:
    title: str
    url: Optional[str] = ""
    children: Optional[Union[List["MenuItem"], Callable]] = None
    check_func: Optional[Callable] = None
    visible: bool = True
    open: bool = False
    selected: bool = False
    parent: Optional["MenuItem"] = None

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"<MenuItem: {self.title}>"

    def check(self, request):
        """set visible flag for the MenuItem"""
        if callable(self.check_func):
            self.visible = self.check_func(request)

    def render(self, request):
        self.check(request)

        if not self.visible:
            return

        if (
            request.resolver_match
            and request.resolver_match.url_name in resolve(self.url).url_name
        ):
            self.selected = True

        if callable(self.children):
            children = list(self.children(request))
        else:
            children = self.children or []

        for child in children:
            child.parent = self
            child.render(request)

        self.children = [child for child in children if child.visible]

        selected = None
        for child in self.children:
            if (
                child.url
                and request.resolver_match
                and request.resolver_match.url_name in resolve(child.url).url_name
            ):
                selected = child

        if selected:
            while selected.parent:
                selected.parent.open = True
                selected = selected.parent


@dataclass(kw_only=True)
class DashboardMenuItem(MenuItem):
    """MenuItem which expects a Dashboard class to check permissions against.  Ignores other check_func"""

    dashboard: Union[Type[Dashboard], Type[ModelDashboard]]

    def check(self, request):
        """only visible if the user has access to the dashboard"""
        self.visible = self.dashboard.has_permissions(request, handle=False)
