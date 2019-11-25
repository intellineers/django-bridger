from rest_framework import serializers

from .mixins import BridgerSerializerFieldMixin
from .types import BridgerType


class ListField(BridgerSerializerFieldMixin, serializers.ListField):
    field_type = BridgerType.LIST.value
