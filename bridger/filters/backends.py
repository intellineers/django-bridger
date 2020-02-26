from django_filters.rest_framework import DjangoFilterBackend as StandardFilterBackend

from .filterset import FilterSet


class DjangoFilterBackend(StandardFilterBackend):
    filterset_base = FilterSet

    # def get_filterset_class(self, view, queryset=None):
    #     print(queryset.model)
    #     rv = super().get_filterset_class(view, queryset)
    #     print(rv)
    #     return rv
