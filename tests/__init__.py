from bridger.menus import default_registry, PresetMenuItem, Menu, MenuItem

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
                add=MenuItem(label="Add Something", endpoint="modeltest-list"),
            ),
            MenuItem(label="Calendar", endpoint="calendar-list",),
            MenuItem(label="PANDAS", endpoint="pandas_view",),
        ],
    )
)
