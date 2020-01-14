import pytest


from tests.viewsets import ModelTestModelViewSet
from rest_framework.test import APIRequestFactory


@pytest.mark.django_db
class TestMetadata:
    def test_metadata_instance(self):
        request = APIRequestFactory().options("")
        vs = ModelTestModelViewSet.as_view({"get": "retrieve"})
        response = vs(request, pk=1)
        assert response.data

    def test_metadata_instance(self):
        request = APIRequestFactory().options("")
        vs = ModelTestModelViewSet.as_view({"get": "retrieve"})
        response = vs(request)
        assert response.data

