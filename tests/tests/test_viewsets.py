import pytest

from bridger.viewsets import ChartViewSet, ModelViewSet, RepresentationModelViewSet

from ..models import ModelTest


@pytest.mark.django_db
def test_model():
    obj = ModelTest.get_random_instance()
    assert obj.id is not None


class TestRepresentationModelViewSet:
    def test_as_view_list(self):
        serializer = RepresentationModelViewSet.as_view({"get": "list"})
        assert serializer

    def test_as_view_instance(self):
        serializer = RepresentationModelViewSet.as_view({"get": "retrieve"})
        assert serializer


class TestModelViewSet:
    def test_as_view_list(self):
        serializer = ModelViewSet.as_view({"get": "list"})
        assert serializer

    def test_as_view_instance(self):
        serializer = ModelViewSet.as_view({"get": "retrieve"})
        assert serializer


class TestChartViewSet:
    def test_as_view_list(self):
        serializer = ChartViewSet.as_view({"get": "list"})
        assert serializer
