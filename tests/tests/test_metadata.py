import pytest
from rest_framework.test import APIRequestFactory

from tests.viewsets import ModelTestModelViewSet

from .utils import AuthenticatedTest


@pytest.mark.django_db
class TestMetadata(AuthenticatedTest):
    def test_metadata_instance(self):
        request = self.blank_options_request
        vs = ModelTestModelViewSet.as_view({"get": "retrieve"})
        response = vs(request, pk=1)
        assert response.data

    def test_metadata_list(self):
        request = self.blank_options_request
        vs = ModelTestModelViewSet.as_view({"get": "list"})
        response = vs(request)
        assert response.data
