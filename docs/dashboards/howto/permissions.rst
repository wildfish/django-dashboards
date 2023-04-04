===========
Permissions
===========

When using the built in routing/views permissions can be set on ``Dashboard`` by either adding a
``permissions_classes`` e.g:

::

    class AdminDashboard(Dashboard):
        admin_text = Text(value="Admin Only Text")

        class Meta:
            name = "Admin Only"
            permission_classes = [IsAdminUser]


or applying global permissions classes with by adding the following to your settings.py

::

    DASHBOARDS_DEFAULT_PERMISSION_CLASSES = ["dashboards.permissions.IsAdminUser"]


Built in permission classes
===========================

All built in permissions function in a similar way to Django's own ``PermissionRequiredMixin`` in that by default
they will redirect to ``settings.LOGIN_URL`` or the ``login_url`` defined on the class.

If a user is logged in but has no access a ``PermissionDenied`` with the message from the permission_denied_message included.

``AllowAny``

Dashboard(s) are accessible to all users (default)

``IsAuthenticated``

Dashboard(s) are accessible to authenticated users only

``IsAdminUser``

Dashboard(s) are accessible to authenticated admin (is_staff=True) users only

Custom permissions
==================

For more granular permission control, subclass one of the built in permissions or
``dashboards.permission.BasePermission``. For example:

::

    class UserHasPerm(BasePermission):
        def has_permission(self, request: HttpRequest, dashboard: Dashboard) -> bool:
            return request.user.has_perm('app_name.can_view_dashboards')

        def handle_no_permission(self, request: HttpRequest, dashboard: Dashboard) -> Union[PermissionDenied, HttpResponseRedirect]:
            # or change how an invalid permission is handled.
            return HttpResponseRedirect(reverse("permission_denied"))


Custom views
============

If you wish to include or combine your dashboards into alternate Django views,
you will need to hook up permissions as required. For example, the internal views
check at ``dispatch()`` with:

::

        has_perm = dashboard_class.has_permissions(
            request=request,
            handle=True
        )
        if not isinstance(has_perm, bool):
            return has_perm
        elif not has_perm:
            raise PermissionDenied()
        ## continue with access

.. note::
    ``has_permissions`` is used, which checks ``has_permission`` for all the ``permission_classes``
    assigned to the dashboard or permissions setting.

``handled`` controls whether or not ``has_permissions`` should call ``handle_no_permission``
on the permission class or simply return False when ``has_permission`` fails.

