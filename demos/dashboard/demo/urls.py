from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

import django_eventstream
from strawberry.django.views import GraphQLView

from wildcoeus.dashboards import config

from .schema import schema


admin.autodiscover()

urlpatterns = [
    path(
        "",
        include(
            "demo.kitchensink.urls",
            namespace="kicthensink",
        ),
    ),
    path(
        f"{config.Config().WILDCOEUS_DASHBOARD_URL}/",
        include("wildcoeus.dashboards.urls"),
    ),
    path("admin/", admin.site.urls),
    path("graphql/", GraphQLView.as_view(schema=schema)),
]

urlpatterns += [
    path("events/", include(django_eventstream.urls), {"channels": ["test"]})
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.ENABLE_SILK:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
