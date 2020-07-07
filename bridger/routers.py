from rest_framework.routers import DefaultRouter, DynamicRoute, Route


class BridgerRouter(DefaultRouter):
    """
    The default Django Rest Framework router with a destroy_multiple method
    """

    routes = [
        # List route.
        Route(
            url=r"^{prefix}{trailing_slash}$",
            mapping={"get": "list", "post": "create", "delete": "destroy_multiple"},
            name="{basename}-list",
            detail=False,
            initkwargs={"suffix": "List"},
        ),
        # Dynamically generated list routes. Generated using
        # @action(detail=False) decorator on methods of the viewset.
        DynamicRoute(url=r"^{prefix}/{url_path}{trailing_slash}$", name="{basename}-{url_name}", detail=False, initkwargs={},),
        # Detail route.
        Route(
            url=r"^{prefix}/{lookup}{trailing_slash}$",
            mapping={"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy",},
            name="{basename}-detail",
            detail=True,
            initkwargs={"suffix": "Instance"},
        ),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        DynamicRoute(
            url=r"^{prefix}/{lookup}/{url_path}{trailing_slash}$", name="{basename}-{url_name}", detail=True, initkwargs={},
        ),
        Route(
            url=r"^{prefix}/{lookup}/history{trailing_slash}$",
            mapping={"get": "history_list"},
            name="{basename}-history-list",
            detail=False,
            initkwargs={"suffix": "History List", "historical_mode": True},
        ),
        Route(
            url=r"^{prefix}/{lookup}/history/(?P<history_id>[^/.]+){trailing_slash}$",
            mapping={"get": "history_retrieve",},
            name="{basename}-history-detail",
            detail=True,
            initkwargs={"suffix": "History Instance", "historical_mode": False},
        ),
    ]
