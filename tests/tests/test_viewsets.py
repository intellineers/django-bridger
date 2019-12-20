import pytest

from bridger.viewsets import ChartViewSet, ModelViewSet, RepresentationModelViewSet


@pytest.mark.django_db
def test_model(model_test):
    assert model_test.id is not None


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
