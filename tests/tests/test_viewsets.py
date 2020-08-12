import pytest

from bridger.viewsets import ChartViewSet, ModelViewSet, RepresentationViewSet


@pytest.mark.django_db
def test_model(model_test):
    assert model_test.id is not None


class TestRepresentationViewSet:
    def test_as_view_list(self):
        viewset = RepresentationViewSet.as_view({"get": "list"})
        assert viewset

    def test_as_view_instance(self):
        viewset = RepresentationViewSet.as_view({"get": "retrieve"})
        assert viewset


class TestModelViewSet:
    def test_as_view_list(self):
        viewset = ModelViewSet.as_view({"get": "list"})
        assert viewset

    def test_as_view_instance(self):
        viewset = ModelViewSet.as_view({"get": "retrieve"})
        assert viewset


class TestChartViewSet:
    def test_as_view_list(self):
        viewset = ChartViewSet.as_view({"get": "list"})
        assert viewset
