from bridger.menus import Menu, MenuItem, PresetMenuItem, default_registry
from celery_app import app as celery_app

# default_registry.register(PresetMenuItem(label="News", preset="StainlyNewsWidget"))
default_registry.register(
    Menu(
        label="Our Menu",
        items=[
            MenuItem(
                label="M1",
                endpoint="modeltest-list",
                add=MenuItem(label="Add Something", endpoint="modeltest-list"),
            ),
            MenuItem(
                label="RM1",
                endpoint="relatedmodeltest-list",
                add=MenuItem(label="Add Something", endpoint="relatedmodeltest-list"),
            ),
            MenuItem(label="Calendar", endpoint="calendar-list",),
            MenuItem(label="PANDAS", endpoint="pandas_view",),
            MenuItem(label="CHART", endpoint="modelchart-list",),
            MenuItem(
                label="History",
                endpoint="relatedmodeltest-history",
                endpoint_args=[259],
            ),
        ],
    )
)
