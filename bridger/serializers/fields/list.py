from rest_framework import serializers
from rest_framework.fields import empty

from .mixins import BridgerSerializerFieldMixin
from .types import BridgerType


class ListField(BridgerSerializerFieldMixin, serializers.ListField):
    field_type = BridgerType.LIST.value

    def run_validation(self, data=empty):
        
        if data not in [None, empty] and len(data) == 1 and isinstance(data[0], str) and "," in data[0]:
            data = data[0].split(",")

        return super().run_validation(data)