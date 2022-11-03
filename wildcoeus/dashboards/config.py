from django.conf import settings


class Config:
    @property
    def WILDCOEUS_DEFAULT_PERMISSION_CLASSES(cls) -> list[str]:
        return getattr(
            settings,
            "WILDCOEUS_DEFAULT_PERMISSION_CLASSES",
            ["wildcoeus.dashboards.permissions.AllowAny"],
        )

    @property
    def WILDCOEUS_DASHBOARD_URL(cls) -> str:
        return getattr(
            settings,
            "WILDCOEUS_DASHBOARD_URL",
            "dashboard",
        )

    @property
    def WILDCOEUS_GRID_PREFIX(cls) -> str:
        return getattr(
            settings,
            "WILDCOEUS_GRID_PREFIX",
            "span",
        )
