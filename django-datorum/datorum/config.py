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
    def DASHBOARD_URL(cls) -> str:
        return getattr(
            settings,
            "DASHBOARD_URL",
            "dashboard",
        )
