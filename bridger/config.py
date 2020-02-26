from typing import Callable, Iterable


class BridgerConfig:
    def __init__(self):
        self._config_list = []

    def register(self, func: Callable):
        self._config_list.append(func)

    def serialize(self, request) -> Iterable:
        for func in self._config_list:
            yield func(request)


config_registry = BridgerConfig()


@config_registry.register
def do_something():
    return "notification", {"hello": "world"}


# print(config_registry.serialize())

# for k in config_registry:
#     print(k)
