from typing import Dict

from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.relations import ManyRelatedField
from rest_framework.request import Request

from .mixins import BridgerSerializerFieldMixin
from .types import BridgerType, ReturnContentType


class BridgerManyRelatedField(ManyRelatedField):
    def __init__(self, *args, **kwargs):
        required = kwargs.get("required", True)
        if not required:
            kwargs["allow_null"] = True
        super().__init__(*args, **kwargs)

    def run_validation(self, data=empty):
        if data is None and self.allow_null:
            data = []
        return super().run_validation(data)

    def get_representation(self, request: Request, field_name: str) -> Dict:
        representation = self.child_relation.get_representation(request, field_name)
        representation["multiple"] = True
        return representation


class PrimaryKeyRelatedField(
    BridgerSerializerFieldMixin, serializers.PrimaryKeyRelatedField
):

    MANY_RELATION_KWARGS = (
        "read_only",
        "write_only",
        "required",
        "default",
        "initial",
        "source",
        "label",
        "help_text",
        "style",
        "error_messages",
        "allow_empty",
        "html_cutoff",
        "html_cutoff_text",
        "allow_null",
    )

    def __init__(self, *args, **kwargs):
        self.field_type = kwargs.pop("field_type", BridgerType.SELECT.value)
        super().__init__(*args, **kwargs)

    def __new__(cls, *args, **kwargs):
        kwargs["style"] = {"base_template": "input.html"}
        return super().__new__(cls, *args, **kwargs)

    @classmethod
    def many_init(cls, *args, **kwargs):
        list_kwargs = {"child_relation": cls(*args, **kwargs)}
        for key in kwargs:
            if key in cls.MANY_RELATION_KWARGS:
                list_kwargs[key] = kwargs[key]
        return BridgerManyRelatedField(**list_kwargs)

    def run_validation(self, data=empty):
        if isinstance(data, str) and data == "null":
            data = None

        if data is empty:
            parent_model_id = self.parent.context["view"].kwargs.get(
                f"{self.field_name}_id"
            )
            if parent_model_id:
                data = parent_model_id

        return super().run_validation(data)


class ListSerializer(serializers.ListSerializer):
    """
    A Wrapper around the normal DRF ListSerializer which also return the child representation
    """

    def get_representation(self, request: Request, field_name: str) -> Dict:
        representation = self.child.get_representation(request, field_name)
        representation["multiple"] = True
        return representation
