from rest_framework import serializers

from .mixins import BridgerSerializerFieldMixin
from .types import BridgerType


class DateTimeField(BridgerSerializerFieldMixin, serializers.DateTimeField):
    field_type = BridgerType.DATETIME.value
    # format = "%Y-%m-%d"


class DateField(BridgerSerializerFieldMixin, serializers.DateField):
    field_type = BridgerType.DATE.value


class TimeField(BridgerSerializerFieldMixin, serializers.TimeField):
    field_type = BridgerType.TIME.value
