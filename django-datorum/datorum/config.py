from django.conf import settings


class Config:
    @property
    def DATORUM_DEFAULT_PERMISSION_CLASSES(cls) -> list[str]:
        return getattr(
            settings,
            "DATORUM_DEFAULT_PERMISSION_CLASSES",
            ["datorum.permissions.AllowAny"],
        )

    @property
    def DATORUM_DASHBOARD_URL(cls) -> str:
        return getattr(
            settings,
            "DATORUM_DASHBOARD_URL",
            "dashboard",
        )

    @property
    def DATORUM_GRID_PREFIX(cls) -> str:
        return getattr(
            settings,
            "DATORUM_GRID_PREFIX",
            "span",
        )
