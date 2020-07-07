from rest_framework import serializers

from .mixins import BridgerSerializerFieldMixin
from .types import BridgerType


class ChoiceField(BridgerSerializerFieldMixin, serializers.ChoiceField):
    field_type = BridgerType.SELECT.value

    def get_representation(self, request, field_name):
        representation = super().get_representation(request, field_name)
        representation["choices"] = [{"value": k, "label": v} for k, v in self.choices.items()]
        return representation
