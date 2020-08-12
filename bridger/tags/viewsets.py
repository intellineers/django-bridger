from bridger.viewsets import RepresentationViewSet

from .models import Tag
from .serializers import TagRepresentationSerializer


class TagRepresentationViewSet(RepresentationViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagRepresentationSerializer

    search_fields = ["title"]
