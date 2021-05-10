from bridger import serializers

from .models import Tag


class TagRepresentationSerializer(serializers.RepresentationSerializer):
    class Meta:
        model = Tag
        read_only_fields = ("slug",)
        fields = ("id", "title", "color", "slug")


class TagSerializerMixin(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), label="Tags", many=True)
    _tags = TagRepresentationSerializer(source="tags", many=True)
