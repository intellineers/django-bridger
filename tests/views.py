# TODO: Delete in favor of viewsets.py
from bridger.viewsets import ModelViewSet
from .serializers import ModelTestSerializer
from .models import ModelTest


def test_response(request):
    return "Test"


class ModelTestViewSet(ModelViewSet):
    serializer_class = ModelTestSerializer
    queryset = ModelTest.objects.all()

    def get_aggregates(self, queryset, paginated_queryset):
        return {"field": {"Sum": 100}}
