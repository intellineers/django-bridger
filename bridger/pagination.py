from django.db.models import QuerySet
from rest_framework.pagination import CursorPagination as DefaultCursorPagination
from rest_framework.pagination import LimitOffsetPagination as DefaultLimitOffsetPagination
from rest_framework.pagination import BasePagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import View


class CursorPagination(DefaultCursorPagination):
    """
    A pagination class that mimics the default Django Rest Framework pagination class,
    but adds functionality to also display aggregated values
    """

    page_size = 25

    def is_initial(self):
        return self.cursor is None

    def _get_position_from_instance(self, instance, ordering):
        new_ordering = [*ordering]
        new_ordering[0] = new_ordering[0].split("__")[0]
        return super()._get_position_from_instance(instance, new_ordering)


class LimitOffsetPagination(DefaultLimitOffsetPagination):

    default_limit = 25
