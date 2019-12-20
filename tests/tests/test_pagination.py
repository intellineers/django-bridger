import pytest
from rest_framework.test import APIRequestFactory

from tests.models import ModelTest
from tests.viewsets import ModelTestModelViewSet


@pytest.mark.django_db
class TestCursorPagination:
    def setup_method(self):
        self.view = ModelTestModelViewSet.as_view({"get": "list"})
        self.factory = APIRequestFactory()

    def test_aggregation(self, model_test):
        request = self.factory.get("")
        response = self.view(request)

        assert response.data["aggregates"] is not None

