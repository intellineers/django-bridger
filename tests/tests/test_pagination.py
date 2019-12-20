import pytest
from rest_framework.test import APIRequestFactory

from ..models import ModelTest
from ..views import ModelTestViewSet


@pytest.mark.django_db
class TestCursorPagination:
    def setup_method(self):
        self.view = ModelTestViewSet.as_view({"get": "list"})
        self.factory = APIRequestFactory()

    def test_aggregation(self, model_test):
        request = self.factory.get("")
        response = self.view(request)

        print(response.data)
        assert response.data["aggregates"] == {"field": {"Sum": 100}}

