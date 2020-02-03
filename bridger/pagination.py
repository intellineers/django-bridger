from django.db.models import QuerySet
from rest_framework.pagination import \
    CursorPagination as DefaultCursorPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import View


class CursorPagination(DefaultCursorPagination):
    """
    A pagination class that mimics the default Django Rest Framework pagination class,
    but adds functionality to also display aggregated values
    """

    page_size = 25

    def paginate_queryset(self, queryset, request, view=None):
        paginated_queryset = super().paginate_queryset(queryset, request, view)

        if hasattr(view, "get_aggregates"):
            self.aggregates = view.get_aggregates(queryset, paginated_queryset)

        if hasattr(view, "get_messages"):
            self.messages = view.get_messages(request, queryset, paginated_queryset)

        return paginated_queryset

    def get_paginated_response(self, data):
        paginated_response = super().get_paginated_response(data)

        if hasattr(self, "aggregates") and self.aggregates:
            paginated_response.data["aggregates"] = self.aggregates

        if hasattr(self, "messages") and self.messages:
            paginated_response.data["messages"] = self.messages

        return paginated_response
