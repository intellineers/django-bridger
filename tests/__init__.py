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
                        label="M1", endpoint="modeltest-list", add=MenuItem(label="Add Something", endpoint="modeltest-list"),
                    ),
                ],
            ),
            MenuItem(
                label="RM1",
                endpoint="relatedmodeltest-list",
                add=MenuItem(label="Add Something", endpoint="relatedmodeltest-list",  permission=ItemPermission(permissions=["tests.add_relatedmodeltest"])),
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
            MenuItem(label="Pandas", endpoint="pandas_view",),
            MenuItem(label="Chart", endpoint="modelchart-list",),
        ],
        index=2,
    ),
)
