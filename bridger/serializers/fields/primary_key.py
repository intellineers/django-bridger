from rest_framework import serializers

from .mixins import BridgerSerializerFieldMixin
from .types import BridgerType


class PrimaryKeyField(BridgerSerializerFieldMixin, serializers.IntegerField):
    field_type = BridgerType.PRIMARY_KEY.value

    def __init__(self, *args, **kwargs):
        kwargs["read_only"] = True
        kwargs["required"] = False
        super().__init__(*args, **kwargs)


class PrimaryKeyCharField(BridgerSerializerFieldMixin, serializers.CharField):
    field_type = BridgerType.PRIMARY_KEY.value

    def __init__(self, *args, **kwargs):
        kwargs["read_only"] = True
        kwargs["required"] = False
        super().__init__(*args, **kwargs)
