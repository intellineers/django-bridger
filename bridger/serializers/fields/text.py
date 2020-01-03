from rest_framework import serializers

from .mixins import BridgerSerializerFieldMixin
from .types import BridgerType, ReturnContentType


class CharField(BridgerSerializerFieldMixin, serializers.CharField):
    field_type = BridgerType.TEXT.value

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


class StringRelatedField(BridgerSerializerFieldMixin, serializers.StringRelatedField):
    field_type = BridgerType.TEXT.value


class TextField(CharField):
    field_type = BridgerType.TEXTEDITOR.value
    texteditor_content_type = ReturnContentType.HTML.value

    def get_representation(self, request, field_name):
        representation = super().get_representation(request, field_name)
        representation["content_type"] = self.texteditor_content_type
        return representation
