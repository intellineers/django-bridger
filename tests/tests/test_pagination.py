import pytest

from rest_framework.views import View

from bridger.pagination import CursorPagination
from ..models import ModelTest


class TestCursorPagination:
    def setup_method(self):
        class SomeView(View):
            pagination_class = CursorPagination
            queryset = ModelTest.objects.all()

            def get_aggregates(self, queryset, paginated_queryset):
                return {"field": {"Sum": 100}}

            def get_aggregates(self, queryset, paginated_queryset):
                return {"field": {"Sum": 100}}

        self.SomeView = SomeView

