from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

import django_eventstream


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
        "dashboard/",
        include("wildcoeus.dashboards.urls"),
    ),
    path("admin/", admin.site.urls),
]

urlpatterns += [
    path("events/", include(django_eventstream.urls), {"channels": ["test"]})
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.ENABLE_SILK:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
