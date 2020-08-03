# from django.test import RequestFactory
# from bridger.menus.registry import default_registry

# def get_menu_items(menus, items, path, level=0):
#     for menu in menus:
#         _path = list([*path])
#         _path.append(menu["label"])
#         if menu_items := menu.get("items"):
#             get_menu_items(menu_items, items, _path, level+1)
#         if "endpoint" in menu:
#             items.append(_path)
#     return items

# def menu_items_for_user(user):
#     request = RequestFactory().get("/")
#     request.user = user
#     default_registry.request = request

#     return get_menu_items(list(default_registry), list(), list())


# def xpath_element_with_class(element: str, class_name: str) -> str:
#     return f"//{element}[@class, '{class_name}']"