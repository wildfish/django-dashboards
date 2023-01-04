import django_eventstream
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


admin.autodiscover()

urlpatterns = [
    path("", include("demo.repos.urls", namespace="repos")),
    path('dashboards/', include('wildcoeus.dashboards.urls')),
    path("pipelines/", include("wildcoeus.pipelines.urls")),
    path("admin/", admin.site.urls),
    path(
        'events/',
        include(django_eventstream.urls),
        {"channels": ["test"]},
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.ENABLE_SILK:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
