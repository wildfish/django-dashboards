from typing import Union
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import resolve_url


class BasePermission:
    """
    Mostly ported from PermissionRequiredMixin but on a per permissions basis
    """

    login_url: str = ""
    permission_denied_message: str = ""
    raise_exception: bool = False
    redirect_field_name: str = "next"

    def has_permission(self, request: HttpRequest, dashboard) -> bool:
        return False

    def get_login_url(self):
        """
        Override this method to override the login_url attribute.
        """
        login_url = self.login_url or settings.LOGIN_URL
        if not login_url:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the login_url attribute. Define "
                f"{self.__class__.__name__}.login_url, settings.LOGIN_URL, or override "
                f"{self.__class__.__name__}.get_login_url()."
            )
        return str(login_url)

    def get_permission_denied_message(self) -> str:
        """
        Override this method to override the permission_denied_message attribute.
        """
        return self.permission_denied_message

    def get_redirect_field_name(self):
        """
        Override this method to override the redirect_field_name attribute.
        """
        return self.redirect_field_name

    def handle_no_permission(
        self, request: HttpRequest, dashboard
    ) -> Union[PermissionDenied, HttpResponseRedirect]:
        if self.raise_exception or request.user.is_authenticated:
            raise PermissionDenied(self.get_permission_denied_message())

        path = request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())
        # If the login url is the same scheme and net location then use the
        # path as the "next" url.
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (not login_scheme or login_scheme == current_scheme) and (
            not login_netloc or login_netloc == current_netloc
        ):
            path = request.get_full_path()
        return redirect_to_login(
            path,
            resolved_login_url,
            self.get_redirect_field_name(),
        )

    def __repr__(self):
        return str(self.__class__.__name__)

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return str(self) == str(other)

        return False


class AllowAny(BasePermission):
    """
    Allows access to anyone.
    """

    def has_permission(self, request, dashboard) -> bool:
        return True


class IsAuthenticated(BasePermission):
    """
    Allows access to authenticated users.
    """

    def has_permission(self, request, dashboard) -> bool:
        return bool(request.user and request.user.is_authenticated)


class IsAdminUser(BasePermission):
    """
    Allows access to staff users.
    """

    def has_permission(self, request, dashboard) -> bool:
        return bool(request.user and request.user.is_staff)
