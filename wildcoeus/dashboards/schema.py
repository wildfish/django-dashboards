import json
from dataclasses import asdict, is_dataclass
from typing import List, Optional

from django.utils.text import slugify

import strawberry
from strawberry.types import Info

from wildcoeus.dashboards.component import Component
from wildcoeus.dashboards.component.layout import HTMLComponentLayout
from wildcoeus.dashboards.dashboard import Dashboard
from wildcoeus.dashboards.registry import registry


class LayoutJSONEncoder(json.JSONEncoder):
    """
    Encode Layout for schema by converting both the:
        - Dataclass objects i.e HTML, HR etc, which have a simple but custom structure.
        - HTMLComponentLayout objects i.e Card, Div which have nested layout of layout_components and eventual
            references to the actual components as str/keys

    TODO would be better if for the dataclasses we change this down the line to exclude things we'd not want in GQL
    for example HTML.html or use a more defined schema for layout.
    """

    def default(self, obj):
        name = obj.__class__.__name__
        if is_dataclass(obj):
            base = asdict(obj)
            base["renderType"] = name
            return base
        if isinstance(obj, HTMLComponentLayout):
            base = obj.__dict__
            base["renderType"] = name
            return base
        return json.JSONEncoder.default(self, obj)


@strawberry.type
class ComponentSchema:
    is_deferred: bool
    key: Optional[str]
    render_type: Optional[str]
    width: Optional[int]

    @strawberry.field()
    def value(self, root: Component, info: Info) -> Optional[strawberry.scalars.JSON]:
        filters = info.variable_values.get("filters", {})
        value = root.get_value(
            request=info.context.get("request"), call_deferred=False, filters=filters
        )
        # convert a django form into a list of field dicts
        if isinstance(value, dict) and "form" in value:
            value["form"] = value["form"].asdict()

        return value


@strawberry.type
class DeferredComponentSchema(ComponentSchema):
    @strawberry.field()
    def value(self, root: Component, info: Info) -> Optional[strawberry.scalars.JSON]:
        filters = info.variable_values.get("filters", {})
        value = root.get_value(
            request=info.context.get("request"), call_deferred=True, filters=filters
        )
        # convert a django form into a list of field dicts
        if isinstance(value, dict) and "form" in value:
            value["form"] = value["form"].asdict()

        return value


@strawberry.type
class DashboardMetaSchema:
    name: str
    dashboard: strawberry.Private[Dashboard]
    slug: str = strawberry.field(resolver=lambda root: slugify(root.name))

    @strawberry.field()
    def layout_json(
        self, root: Dashboard.Layout, info: Info
    ) -> Optional[strawberry.scalars.JSON]:
        if self.dashboard.Layout.components:
            return json.loads(
                json.dumps(
                    self.dashboard.Layout.components.__dict__, cls=LayoutJSONEncoder
                )
            )
        return None


@strawberry.type
class DashboardSchema:
    Meta: DashboardMetaSchema
    components: List[ComponentSchema]


def get_dashboards(info: Info) -> list[DashboardSchema]:
    dashboards = []
    for dashboard_cls in registry.get_graphql_dashboards().values():
        # make sure the current request has access to the dashboard before adding
        if dashboard_cls.has_permissions(request=info.context.get("request")):
            instance = dashboard_cls(request=info.context.get("request"))
            schema = DashboardSchema(
                Meta=DashboardMetaSchema(name=instance.Meta.name, dashboard=instance),
                components=[c for c in instance.get_components() if c.serializable],
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
        self,
        slug: str,
        key: str,
        info: Info,
        filters: Optional[strawberry.scalars.JSON] = None,
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
            return None
        except IndexError:
            return None
