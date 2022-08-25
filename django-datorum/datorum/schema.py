import logging
from typing import List, Optional

from django.utils.text import slugify

import strawberry
from strawberry.types import Info

from datorum.component import Component
from datorum.registry import registry


logger = logging.getLogger(__name__)


@strawberry.type
class ComponentSchema:
    is_deferred: bool
    key: Optional[str]
    render_type: Optional[str]
    width: Optional[int]
    group: Optional[str]
    group_width: Optional[int]

    @strawberry.field()
    def value(self, root: Component, info: Info) -> Optional[strawberry.scalars.JSON]:
        return root.for_render(info.context.get("request"), call_deferred=False)


@strawberry.type
class DeferredComponentSchema(ComponentSchema):
    @strawberry.field()
    def value(self, root: Component, info: Info) -> Optional[strawberry.scalars.JSON]:
        return root.for_render(info.context.get("request"), call_deferred=True)


@strawberry.type
class DashboardSchemaMeta:
    name: str
    slug: str = strawberry.field(resolver=lambda root: slugify(root.name))


@strawberry.type
class DashboardSchema:
    Meta: DashboardSchemaMeta
    components: List[ComponentSchema]


def get_dashboards(info: Info) -> list[DashboardSchema]:
    dashboards = []
    for instance in registry.get_graphql_dashboards().values():
        # make sure the current request has access to the dashboard before adding
        if instance.has_permissions(request=info.context.get("request")):
            schema = DashboardSchema(
                Meta=DashboardSchemaMeta(name=instance.Meta.name),
                components=instance.get_components(),
            )
            dashboards.append(schema)
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
