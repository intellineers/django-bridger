# TODO: Most likely to be removed
from rest_framework import serializers

from .mixins import BridgerSerializerFieldMixin
from .number import IntegerField
from .types import BridgerType, ReturnContentType


class StarRatingField(IntegerField):
    field_type = "starrating"


class RangeSelectField(BridgerSerializerFieldMixin, serializers.FloatField):
    field_type = "rangeselect"

    def __init__(self, *args, **kwargs):
        self.color = kwargs.pop("color", "rgb(133, 144, 162)")
        super().__init__(*args, **kwargs)

    def get_representation(self, request, field_name):
        representation = super().get_representation(request, field_name)
        representation["color"] = self.color
        return representation
