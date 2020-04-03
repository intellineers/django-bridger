from collections import defaultdict
from typing import Any, Callable, Dict, List, NamedTuple, Optional

from django.contrib import admin
from rest_framework.request import Request
from rest_framework.reverse import reverse


class ItemPermission(NamedTuple):
    permissions: List[str] = []
    method: Optional[Callable] = None

    def has_permission(self, request: Request):
        if request.user.is_superuser:
            return True

        for permission in self.permissions:
            if not request.user.has_perm(permission):
                return False

        if self.method:
            return self.method(request=request)

        return True


class PresetMenuItem(NamedTuple):
    label: str
    preset: str
    permission: Optional[ItemPermission] = None

    def to_dict(self, request: Request) -> Dict:
        if self.permission is None or self.permission.has_permission(request):
            return {"label": self.label, "preset": self.preset}
        return None


class MenuItem(NamedTuple):
    label: str
    endpoint: str

    endpoint_args: List = []
    endpoint_kwargs: Dict = {}

    get_params: Dict = {}

    permission: Optional[ItemPermission] = None
    add: Any = None

    def to_dict(self, request: Request) -> Dict:
        if self.permission is None or self.permission.has_permission(request):
            item = {
                "label": self.label,
                "endpoint": reverse(
                    viewname=self.endpoint,
                    request=request,
                    args=self.endpoint_args,
                    kwargs=self.endpoint_kwargs,
                ),
            }

            if self.get_params:
                item["endpoint"] += f"?history_id={self.get_params['history_id']}"

            if self.add:
                item["add"] = self.add.to_dict(request=request)

            return item

        return None


class Menu(NamedTuple):
    label: str
    items: List

    def to_dict(self, request: Request) -> Dict:
        menu_dict = {"label": self.label, "items": list()}
        for item in self.items:
            _item = item.to_dict(request=request)
            if _item:
                menu_dict["items"].append(_item)

        if len(menu_dict["items"]) == 0:
            return None

        return menu_dict


class MenuRegistry:
    def __init__(self):
        self._registry = list()

    def register(self, menu: Menu):
        self._registry.append(menu)

    def to_dict(self, request: Request) -> List:
        menu_list = list()
        for menu in self._registry:
            _menu = menu.to_dict(request=request)
            if _menu is not None:
                menu_list.append(_menu)
        return menu_list


default_registry = MenuRegistry()

# default_registry.register(PresetMenuItem(label="News", preset="StainlyNewsWidget"))

# default_registry.register(
#     Menu(
#         label="Our Menu",
#         items=[
#             MenuItem(
#                 label="M1",
#                 endpoint="e1",
#                 add=MenuItem(label="Add Something", endpoint="ea1"),
#             ),
#             Menu(label="Nested Menu", items=[MenuItem(label="N-M1", endpoint="e1"),],),
#         ],
#     )
# )

# import pprint

# pprint.pprint(default_registry.to_dict(request=None))
