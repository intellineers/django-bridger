from .menus import Menu


class MenuRegistry:
    def __init__(self):
        self._registry = list()

    def register(self, menu: Menu):
        self._registry.append(menu)

    def __iter__(self):
        request = getattr(self, "request", None)
        alphabetical_sorted = getattr(self, "alphabetical_sorted", False)

        key = lambda x: (x.index is None, x.index)

        if alphabetical_sorted:
            key = lambda x: x.label

        for menu in sorted(filter(lambda x: bool(x), self._registry), key=key):
            menu.request = request
            serialized_menu = dict(menu)
            if serialized_menu != {}:
                yield serialized_menu


default_registry = MenuRegistry()
