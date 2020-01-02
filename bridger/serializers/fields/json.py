from rest_framework import serializers

from .mixins import BridgerSerializerFieldMixin
from .types import BridgerType, ReturnContentType


class JSONField(BridgerSerializerFieldMixin, serializers.JSONField):
    field_type = BridgerType.JSON.value


class JSONTextEditorField(BridgerSerializerFieldMixin, serializers.JSONField):
    field_type = BridgerType.TEXTEDITOR.value
    texteditor_content_type = ReturnContentType.JSON.value

    def get_representation(self, request, field_name):
        representation = super().get_representation(request, field_name)
        representation["content_type"] = self.texteditor_content_type
        return representation
