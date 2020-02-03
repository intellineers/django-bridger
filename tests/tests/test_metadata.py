import pytest
from rest_framework.test import APIRequestFactory

from tests.viewsets import ModelTestModelViewSet


@pytest.mark.django_db
class TestMetadata:
    def test_metadata_instance(self):
        request = APIRequestFactory().options("")
        vs = ModelTestModelViewSet.as_view({"get": "retrieve"})
        response = vs(request, pk=1)
        assert response.data

    def test_metadata_list(self):
        request = APIRequestFactory().options("")
        vs = ModelTestModelViewSet.as_view({"get": "retrieve"})
        response = vs(request)
        assert response.data
