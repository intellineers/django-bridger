from django.contrib.postgres.fields import ArrayField
from django.db import models
from rest_framework import serializers

from bridger.serializers import fields

from .mixins import RepresentationSerializerMixin


class ModelSerializer(serializers.ModelSerializer):
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
        ArrayField: fields.ListField,
        fields.StarRatingField: fields.StarRatingField,
    }
    serializer_related_field = fields.PrimaryKeyRelatedField
    serializer_choice_field = fields.ChoiceField


class RepresentationSerializer(RepresentationSerializerMixin, ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.filter_params = kwargs.pop("filter_params", None)

        if hasattr(self.Meta.model, "get_label_key"):
            self.label_key = kwargs.pop("label_key", self.Meta.model.get_label_key())
        else:
            self.label_key = kwargs.pop("label_key", self.label_key)
        super().__init__(*args, **kwargs)
