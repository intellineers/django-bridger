import operator
from functools import reduce

from django.db.models import F, Q, QuerySet, Value
from django.db.models.functions import Concat

search_models = []


class SearchRegistry:
    def __init__(self):
        self._registry = {}

    def register(self, _class, endpoint):
        self._registry[_class.__name__] = {
            "class": _class,
            "verbose_name": _class._meta.verbose_name,
            "endpoint": endpoint,
        }

    def registered_models(self):
        yield from self._registry.items()


registry = SearchRegistry()


def register(endpoint):
    def _search_wrapper(model_class):
        registry.register(model_class, endpoint)
        return model_class

    return _search_wrapper


def search(search_term, request=None):
    qs = None
    for key, values in registry._registry.items():

        # filtering = reduce(
        #     lambda x, y: operator.and_(
        #         Q(__search__icontains=x), Q(__search__icontains=y)
        #     ),
        #     search_term.split(" "),
        # )

        _qs = (
            values["class"]
            .search_for_term(search_term, request)
            .annotate(__search=Concat(F("_search"), Value(f" {values['verbose_name']}")))
        )

        for term in search_term.split(" "):
            _qs = _qs.filter(__search__icontains=term)

        _qs = _qs.values("id", "_repr", "__search")

        if qs is None:
            qs = _qs
        else:
            qs = qs.union(_qs)

    return qs
