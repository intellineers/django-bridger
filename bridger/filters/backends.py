from django_filters.rest_framework import DjangoFilterBackend as StandardFilterBackend

from .filterset import FilterSet


class DjangoFilterBackend(StandardFilterBackend):
    filterset_base = FilterSet

    def get_filterset_class(self, view, queryset=None):

        if method := getattr(view, "get_filterset_class", None):
            view.filterset_class = method(view.request)

        if method := getattr(view, "get_filterset_fields", None):
            view.filterset_fields = method(view.request)

        return super().get_filterset_class(view, queryset)
