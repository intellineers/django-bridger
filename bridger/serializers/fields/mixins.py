import logging
from datetime import datetime

from rest_framework.fields import empty
from rest_framework.settings import api_settings

logger = logging.getLogger(__name__)


class BridgerSerializerFieldMixin:
    """
    A mixin that takes care of adding all the necessary magic to each implementation
    of the serializer fields
    """

    def __init__(self, *args, **kwargs):
        self.extra = kwargs.pop("extra", None)
        self.decorators = kwargs.pop("decorators", [])
        super().__init__(*args, **kwargs)

    def get_representation(self, request, field_name):

        if meta := getattr(self.parent, "Meta", None):
            if field_name in getattr(meta, "required_fields", []):
                self.required = True

        representation = {
            "key": field_name,
            "label": getattr(self, "label", None),
            "type": getattr(self, "field_type", "undefined"),
            "required": getattr(self, "required", True),
            "read_only": getattr(self, "read_only", False),
        }

        default = getattr(self, "default", None)

        if default and default != empty:
            if isinstance(default, datetime):
                default = default.strftime(api_settings.DATETIME_FORMAT)

            representation["default"] = default() if callable(default) else default
        else:
            try:
                default = self.parent.Meta.model._meta._forward_fields_map[field_name].default
                if isinstance(default, (str, float, int)):
                    representation["default"] = default
            except:  # TODO Add some explicit exception handling
                pass

        representation["decorators"] = getattr(self, "decorators", [])

        for _attr in ["help_text", "extra"]:
            attr = getattr(self, _attr, None)
            if attr:
                representation[_attr] = attr

        return representation
