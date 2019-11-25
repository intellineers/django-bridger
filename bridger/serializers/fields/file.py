from rest_framework import serializers

from .mixins import BridgerSerializerFieldMixin
from .types import BridgerType, ReturnContentType


class ImageField(BridgerSerializerFieldMixin, serializers.ImageField):
    field_type = BridgerType.IMAGE.value


class FileField(BridgerSerializerFieldMixin, serializers.FileField):
    field_type = BridgerType.FILE.value
