The bridger has the capability to return menus by adding menus to a registry. By default there is a `bridger.menus.default_registry` where menus can be added which in return can be retrieved through the `bridger:menu` endpoint.

Usually the menu of an app is added to the `__init__.py` of the root directory of each app, but it could be placed at any location that is loaded upon starting the server.

# Structure

blockdiag {
    registry [label="MenuRegistry"];
    menu1 [label="Menu"];
    menu2 [label="Menu"];
    menu3 [label="Menu"];
    menuitem1 [label="MenuItem"];
    menuitem2 [label="MenuItem"];
    menuitem3 [label="MenuItem"];
    menuitem4 [label="MenuItem"];
    menuitem5 [label="MenuItem"];
    menuitem6 [label="MenuItem"];
    itempermission [label="ItemPermission"];
    registry -> menu1;
    registry -> menu2;
                menu1 -> menuitem1;
                menu1 -> menuitem2;
                menu1 -> menu3;
                menu2 -> menuitem3;
                menu2 -> menuitem4;
                         menuitem3 -> itempermission;
                menu3 -> menuitem5;
                menu3 -> menuitem6;
}

# MenuRegistry

Each registry represents one menu group. A registry can register a menu through the `register(menu)` method.

# Menu

Each menu represents one menu that contains several items or nested menus.

# MenuItem

Each menu item represents one actionable item inside of a menu. The action that is run depends on the endpoint of the menu item.

For each menu item a create button can be defined. This is useful if a user should be able to create an instance of a model from the menu (e.g. open a form to create the instance). For this, another menu item has to be attached to the field `add`.

# ItemPermission

Each menu item can have an ItemPermission to determine if the current user that retrieves the menu can retrieve the menuitem.

To determine whether the current user can retrieve the menuitem has to fields that can be evaluated:

1. `permissions`: A list of django permissions that are checked against the current user. Returns `True` if all permissions are valid for the current user, otherwise `False`
2. `method`: A callable that has to accepts the request as a parameter. The callable has to return `True` or `False`

If the current user is a `superuser` the ItemPermission always returns `True`.

# Example

blockdiag {
    registry [label="MenuRegistry"];
    menu1 [label="Menu1"];
    menu2 [label="Menu2"];
    menuitem1 [label="MenuItem1"];
    menuitem2 [label="MenuItem2"];
    menuitem3 [label="MenuItem3"];
    menuitem4 [label="MenuItem4"];
    menuitem4_add [label="Add MenuItem4"];
    itempermission [label="ItemPermission"];
    registry -> menu1;
    registry -> menu2;
                menu1 -> menuitem1;
                menu1 -> menuitem2;
                menu2 -> menuitem3;
                menu2 -> menuitem4;
                         menuitem4 -> menuitem4_add;
                         menuitem3 -> itempermission;
}

```python
# __init__.py
from bridger.menus import default_registry, Menu, MenuItem, ItemPermissions

default_registry.register(
    Menu(label="Menu1", items=[
        MenuItem(label="MenuItem1", endpoint="app:endpoint1"),
        MenuItem(label="MenuItem2", endpoint="app:endpoint2"),
    ])
)

default_registry.register(
    Menu(label="Menu2", items=[
        MenuItem(
            label="MenuItem3",
            endpoint="app:endpoint3",
            permission=ItemPermission(
                method=lambda request: request.user.is_staff
            )
        ),
        MenuItem(
            label="MenuItem4",
            endpoint="app:endpoint4",
            add=MenuItem(label="Add MenuItem4", endpoint="app:endpoint4")
        ),
    ])
)
```