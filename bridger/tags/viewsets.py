from bridger.viewsets import RepresentationModelViewSet

from .models import Tag
from .serializers import TagRepresentationSerializer


class TagRepresentationViewSet(RepresentationModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagRepresentationSerializer

    search_fields = ["title"]
