import functools
import logging
from inspect import getmembers

from rest_framework import serializers
from rest_framework.reverse import reverse

from bridger.signals.instance_buttons import add_additional_resource

from .mixins import BridgerSerializerFieldMixin
from .types import BridgerType

logger = logging.getLogger(__name__)


def register_resource():
    def decorator(func):
        func._is_additional_resource = True
        return func

    return decorator


def _is_additional_resource(attr):
    return hasattr(attr, "_is_additional_resource")


def register_dynamic_button():
    def decorator(func):
        func._is_dynamic_button = True
        return func

    return decorator


def _is_dynamic_button(attr):
    return hasattr(attr, "_is_dynamic_button")


class DynamicButtonField(BridgerSerializerFieldMixin, serializers.ReadOnlyField):

    field_type = "_dynamic_buttons"

    def get_attribute(self, instance):
        return instance

    def to_representation(self, value):
        request = self.parent.context["request"]
        buttons = list()

        for _, button_func in getmembers(self.parent.__class__, _is_dynamic_button):
            btns = button_func(self.parent, instance=value, request=request, user=request.user)
            buttons.extend([dict(btn) for btn in btns])

        return buttons


class AdditionalResourcesField(BridgerSerializerFieldMixin, serializers.ReadOnlyField):

    field_type = "_additional_resources"

    def get_attribute(self, instance):
        return instance

    def to_representation(self, value):
        request = self.parent.context["request"]
        resources = dict()
        for _, function in getmembers(self.parent.__class__, _is_additional_resource):
            _d = function(self.parent, instance=value, request=request, user=request.user)
            resources = {**resources, **_d}

        remote_resources = add_additional_resource.send(
            sender=self.parent.__class__, serializer=self.parent, instance=value, request=request, user=request.user
        )
        for _, resource in remote_resources:
            resources = {**resources, **resource}

        return resources


class HyperlinkField(BridgerSerializerFieldMixin, serializers.ReadOnlyField):
    def __init__(self, *args, **kwargs):
        self.reverse_name = kwargs.pop("reverse_name")
        super().__init__(*args, **kwargs)

    def get_attribute(self, obj):
        request = self.context.get("request", None)
        if request:
            return reverse(self.reverse_name, args=[obj.id], request=request)
        return reverse(self.reverse_name, args=[obj.id])


class ReadOnlyField(BridgerSerializerFieldMixin, serializers.ReadOnlyField):
    field_type = BridgerType.TEXT.value


class SerializerMethodField(BridgerSerializerFieldMixin, serializers.SerializerMethodField):
    def __init__(self, method_name=None, field_type=BridgerType.TEXT.value, **kwargs):
        self.field_type = field_type
        super().__init__(method_name, **kwargs)
