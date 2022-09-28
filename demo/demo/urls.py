from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

import django_eventstream
from strawberry.django.views import GraphQLView

from .demo_app.schema import schema


admin.autodiscover()

urlpatterns = [
    path(
        "",
        include(
            "demo.demo_app.urls",
            namespace="demo_app",
        ),
    ),
    path("dashboard/", include("datorum.urls")),
    path("admin/", admin.site.urls),
    path("graphql/", GraphQLView.as_view(schema=schema)),
]

urlpatterns += [
    path("events/", include(django_eventstream.urls), {"channels": ["test"]})
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
