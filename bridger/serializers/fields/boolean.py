from rest_framework import serializers

from .mixins import BridgerSerializerFieldMixin
from .types import BridgerType


class BooleanField(BridgerSerializerFieldMixin, serializers.BooleanField):
    field_type = BridgerType.BOOLEAN.value
