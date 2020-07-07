from typing import Dict

from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django_fsm import FSMField
from rest_framework import serializers
from rest_framework.request import Request

from bridger.fsm.mixins import FSMSerializerMetaclass
from bridger.serializers import fields

from .mixins import RepresentationSerializerMixin


def decorator(position: str, value: str) -> Dict:
    assert position in ("left", "right"), "Decorator Position can only be right or left"
    return {"position": position, "value": value}


percent_decorator = decorator(position="right", value="%")


class AdditionalMetadataMixin:
    @classmethod
    def get_decorators(cls):
        if hasattr(cls, "Meta"):
            yield from getattr(cls.Meta, "decorators", dict()).items()

    @classmethod
    def get_percent_fields(cls):
        if hasattr(cls, "Meta"):
            yield from getattr(cls.Meta, "percent_fields", list())


class Serializer(AdditionalMetadataMixin, serializers.Serializer):
    pass


class ModelSerializer(
    AdditionalMetadataMixin, serializers.ModelSerializer, metaclass=FSMSerializerMetaclass,
):

    serializer_field_mapping = {
        models.AutoField: fields.PrimaryKeyField,
        models.BooleanField: fields.BooleanField,
        models.CharField: fields.CharField,
        models.DateField: fields.DateField,
        models.DateTimeField: fields.DateTimeField,
        models.TimeField: fields.TimeField,
        models.DecimalField: fields.DecimalField,
        models.FileField: fields.FileField,
        models.FloatField: fields.FloatField,
        models.ImageField: fields.ImageField,
        models.IntegerField: fields.IntegerField,
        models.PositiveIntegerField: fields.IntegerField,
        models.PositiveSmallIntegerField: fields.IntegerField,
        models.SmallIntegerField: fields.IntegerField,
        models.TextField: fields.TextField,
        models.UUIDField: fields.CharField,
        ArrayField: fields.ListField,
        JSONField: fields.JSONField,
        fields.StarRatingField: fields.StarRatingField,
    }
    serializer_related_field = fields.PrimaryKeyRelatedField
    serializer_choice_field = fields.ChoiceField
    serializer_fsm_field = fields.FSMStatusField

    _additional_resources = fields.AdditionalResourcesField()
    _buttons = fields.DynamicButtonField()

    def build_standard_field(self, field_name, model_field):
        field_class, field_kwargs = super().build_standard_field(field_name, model_field)
        if isinstance(model_field, FSMField):
            field_class = self.serializer_fsm_field

        return field_class, field_kwargs

    def build_property_field(self, field_name, model_class):
        field_class = fields.ReadOnlyField
        field_kwargs = {}

        return field_class, field_kwargs


class RepresentationSerializer(RepresentationSerializerMixin, ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.filter_params = kwargs.pop("filter_params", getattr(self, "filter_params", None))

        self.endpoint = kwargs.pop("endpoint", getattr(self, "endpoint", self.Meta.model.get_representation_endpoint()),)

        self.value_key = kwargs.pop("value_key", getattr(self, "value_key", self.Meta.model.get_representation_value_key()),)

        self.label_key = kwargs.pop("label_key", getattr(self, "label_key", self.Meta.model.get_representation_label_key()),)

        super().__init__(*args, **kwargs)
