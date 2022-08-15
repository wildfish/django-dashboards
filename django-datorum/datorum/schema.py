import logging
from typing import List, Optional

from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.text import slugify

import strawberry
from strawberry.types import Info

from datorum.component import Component


logger = logging.getLogger(__name__)


@strawberry.type
class ComponentSchema:
    is_deferred: bool
    key: Optional[str]
    render_type: Optional[str]
    width: Optional[int]
    value: Optional[strawberry.scalars.JSON]
    group: Optional[str]
    group_width: Optional[int]


@strawberry.type
class DeferredComponentSchema(ComponentSchema):
    @strawberry.field()
    def value(self, root: Component, info: Info) -> Optional[strawberry.scalars.JSON]:
        return root.for_render(info.context.request)


@strawberry.type
class DashboardSchemaMeta:
    name: str
    slug: str = strawberry.field(resolver=lambda root: slugify(root.name))


@strawberry.type
class DashboardSchema:
    Meta: DashboardSchemaMeta
    components: List[ComponentSchema]


def get_dashboards(info: Info) -> list[DashboardSchema]:
    """
    For now read them in via a setting, some sort of registry with include_in_graphql would better.
    Returns:

    """
    dashboards = []
    for d in settings.DATORUM_GRAPHQL_DASHBOARDS:
        try:
            instance = import_string(d)(request=info.context.request)
            schema = DashboardSchema(
                Meta=DashboardSchemaMeta(name=instance.Meta.name),
                components=instance.get_components(),
            )
            dashboards.append(schema)
        except (ModuleNotFoundError, ImportError):
            logger.error(f"{d} is not a valid dashboard path")

    return dashboards


@strawberry.type
class DashboardQuery:
    dashboards: List[DashboardSchema] = strawberry.field(resolver=get_dashboards)

    @strawberry.field
    def dashboard(self, slug: str, info: Info) -> Optional[DashboardSchema]:
        try:
            dashboard = [
                d for d in get_dashboards(info) if slug == slugify(d.Meta.name)
            ][0]
            return dashboard
        except IndexError:
            return None

    @strawberry.field
    def component(
        self, slug: str, key: str, info: Info
    ) -> Optional[DeferredComponentSchema]:
        try:
            dashboard = [
                d for d in get_dashboards(info) if slug == slugify(d.Meta.name)
            ][0]
            for component_schema in dashboard.components:
                if component_schema.key == key:
                    # Changing the type to DeferredComponentSchema makes this return what we expect, but
                    # causes a mypy issue, need to look at how we resolve this, but it is working as expected.
                    return component_schema  # type: ignore
        except IndexError:
            return None
        return None
