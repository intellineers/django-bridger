from bridger import serializers

from .models import Tag


class TagRepresentationSerializer(serializers.RepresentationSerializer):
    class Meta:
        model = Tag
        fields = ("id", "title", "color")


class TagSerializerMixin(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), label="Tags", many=True)
    _tags = TagRepresentationSerializer(source="tags", many=True)
