from bridger.menus import ItemPermission, Menu, MenuItem, default_registry
from celery_app import app as celery_app


default_registry.alphabetical_sorted = True
default_registry.register(
    Menu(
        label="Normal Views",
        items=[
            Menu(
                label="Sub Normal Views",
                items=[
                    MenuItem(
                        label="M1",
                        endpoint="modeltest-list",
                        add=MenuItem(label="Add Something", endpoint="modeltest-list"),
                    ),
                ],
            ),
            MenuItem(
                label="RM1",
                endpoint="relatedmodeltest-list",
                add=MenuItem(label="Add Something", endpoint="relatedmodeltest-list"),
            ),
        ],
        index=1,
    ),
)
default_registry.register(
    Menu(
        label="Special Views",
        items=[
            MenuItem(label="Calendar", endpoint="calendar-list",),
            MenuItem(label="PANDAS", endpoint="pandas_view",),
            MenuItem(label="Clubhouse", endpoint="bridger:clubhouse-list",),
            # MenuItem(label="CHART", endpoint="modelchart-list",),
        ],
        index=2,
    ),
)
