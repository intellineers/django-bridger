from bridger.viewsets import RepresentationModelViewSet
from .serializers import TagRepresentationSerializer
from .models import Tag


class TagRepresentationViewSet(RepresentationModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagRepresentationSerializer

    search_fields = ["title"]
