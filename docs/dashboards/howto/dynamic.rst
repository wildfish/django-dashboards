==================
Dynamic dashboards
==================

Instead of defining the components for your Dashboard statically you can
generate them on the fly as part of the ``__init__()`` function.
This allows you to tailor the components you show.

First define you Dashboard with an __init__ function:

::

    # dashboards.py
    from dashboards.dashboard import Dashboard

    class DynamicDashboard(Dashboard):
        def __init__(self, request: HttpRequest, *args, **kwargs):
            super().__init__(request=request, *args, **kwargs)
            ...

You can then manually add any components to the ``self.components`` dictionary:

::

    # dashboards.py
    from dashboards.dashboard import Dashboard

    class DynamicDashboard(Dashboard):
        def __init__(self, request: HttpRequest, *args, **kwargs):
            super().__init__(request=request, *args, **kwargs)

        # Generated components
        for r in range(1, 3):
            self.components[f"dynamic_component_{r}"] = Text(
                value=f"Rendered Dynamically via __init__: {r}")

You can also mix and match how you define components::

    ...

    class DynamicDashboard(Dashboard):
        normal_component = Text(value="hello")

        def __init__(self, request: HttpRequest, *args, **kwargs):
            super().__init__(request=request, *args, **kwargs)

        # Generated components
        for r in range(1, 3):
            self.components[f"dynamic_component_{r}"] = Text(
                value=f"Rendered Dynamically via __init__: {r}")

This creates a dashboard with 4 components: ``normal_component``, ``dynamic_component_1``, ``dynamic_component_2``, ``dynamic_component_3``

This is a simplistic example but a real use case could be if you wanted to hide
components for certain users.  This is possible as the init function
has access the the ``request`` object::

    class DynamicDashboard(Dashboard):
        normal_component = Text(value="hello")

        def __init__(self, request: HttpRequest, *args, **kwargs):
            super().__init__(request=request, *args, **kwargs)

        # only add this component for staff
        if request.user.is_staff:
            self.components["component_for_staff"] = Text(
                value="Only for staff users"
            )

This would show ``normal_component`` to everyone but only include ``component_for_staff``
if the user had the ``is_staff`` flag set.

Another good example of how this could be helpful is if you wish to share data
between components but don't want to have to make multiple calls to the same datasource::

    class DynamicDashboard(Dashboard):
        def __init__(self, request: HttpRequest, *args, **kwargs):
            super().__init__(request=request, *args, **kwargs)

        # run super slow fetch
        data = get_large_dataset()

        self.components["component_for_row0"] = Text(
            value=data[0]["field1"]
        )
        self.components["component_for_row1"] = Text(
            value=data[1]["field1"]
        )

This calls the ``get_large_dataset()`` function once but then passes it to both
``component_for_row0`` and ``component_for_row1`` to render.