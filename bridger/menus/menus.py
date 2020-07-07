from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Union

from django.utils.http import urlencode
from rest_framework.request import Request
from rest_framework.reverse import reverse


@dataclass
class ItemPermission:
    permissions: List[str] = field(default_factory=list)
    method: Optional[Callable] = None

    def has_permission(self, request: Request) -> bool:
        if request.user.is_superuser:
            return True

        for permission in self.permissions:
            if not request.user.has_perm(permission):
                return False

        if self.method:
            return self.method(request=request)

        return True


@dataclass
class MenuItem:
    label: str

    endpoint: str
    endpoint_args: List[str] = field(default_factory=list)
    endpoint_kwargs: Dict[str, str] = field(default_factory=dict)
    endpoint_get_parameters: Dict[str, str] = field(default_factory=dict)
    reverse: bool = True

    permission: Optional[ItemPermission] = None
    add: Optional["MenuItem"] = None

    def __iter__(self):
        request = getattr(self, "request", None)
        if self.permission is None or self.permission.has_permission(request=request):
            if self.reverse:
                endpoint = reverse(
                    viewname=self.endpoint, args=self.endpoint_args, kwargs=self.endpoint_kwargs, request=request,
                )
            else:
                endpoint = self.endpoint

            if self.endpoint_get_parameters:
                endpoint += f"?{urlencode(self.endpoint_get_parameters)}"

            yield "label", self.label
            yield "endpoint", endpoint
            if self.add:
                self.add.request = request
                yield "add", dict(self.add)


@dataclass
class Menu:
    label: str
    items: List[Union[MenuItem, "Menu"]] = field(default_factory=list)

    index: Optional[int] = None

    def __iter__(self):
        request = getattr(self, "request", None)
        items = list()
        for item in filter(lambda x: bool(x), self.items):
            item.request = request
            serialized_item = dict(item)
            if serialized_item:
                items.append(serialized_item)

        if len(items) > 0:
            yield "label", self.label
            yield "items", items
