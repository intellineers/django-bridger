from rest_framework import serializers

from .mixins import BridgerSerializerFieldMixin
from .types import BridgerType


class IntegerField(BridgerSerializerFieldMixin, serializers.IntegerField):
    field_type = BridgerType.NUMBER.value

    def get_representation(self, request, field_name):
        representation = super().get_representation(request, field_name)
        representation["precision"] = 0
        return representation


class DecimalField(BridgerSerializerFieldMixin, serializers.DecimalField):
    field_type = BridgerType.NUMBER.value

    def __init__(self, *args, **kwargs):
        self.percent = kwargs.pop("percent", False)
        super().__init__(*args, **kwargs)

    # TODO: If this is used, then the validation for max_digits and decimal_fields is not done
    # def validate_precision(self, value):
    #     return value

    def get_representation(self, request, field_name):
        representation = super().get_representation(request, field_name)
        representation["precision"] = self.decimal_places

        if self.percent:  # TODO: Discuss with Christoph if this is necessary like this
            representation["type"] = BridgerType.PERCENT.value
            representation["precision"] = self.decimal_places - 2

        return representation


class FloatField(BridgerSerializerFieldMixin, serializers.FloatField):
    field_type = BridgerType.NUMBER.value

    def __init__(self, *args, **kwargs):
        self.decimal_places = kwargs.pop("decimal_places", 2)
        super().__init__(*args, **kwargs)

    def get_representation(self, request, field_name):
        representation = super().get_representation(request, field_name)
        representation["precision"] = self.decimal_places
        return representation
