class BasePermission:
    def has_permission(self, request):  # pragma: no cover
        raise NotImplementedError(
            "Subclasses of BasePermission must provide a has_permission() method."
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

    def has_permission(self, request):
        return True


class IsAuthenticated(BasePermission):
    """
    Allows access to authenticated users.
    """

    def has_permission(self, request):
        return bool(request.user and request.user.is_authenticated)


class IsAdminUser(BasePermission):
    """
    Allows access to staff users.
    """

    def has_permission(self, request):
        return bool(request.user and request.user.is_staff)
