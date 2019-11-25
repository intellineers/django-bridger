from rest_framework.fields import empty


class BridgerSerializerFieldMixin:
    """
    A mixin that takes care of adding all the necessary magic to each implementation
    of the serializer fields
    """

    def __init__(self, *args, **kwargs):
        self.extra = kwargs.pop("extra", None)
        self.decorators = kwargs.pop("decorators", None)
        super().__init__(*args, **kwargs)

    def get_representation(self, request, field_name):
        representation = {
            "key": field_name,
            "label": self.label,
            "type": self.field_type,
            "required": getattr(self, "required", False),
            "read_only": getattr(self, "read_only", False),
        }

        if self.default and self.default != empty:
            if not callable(self.default):
                representation["default"] = self.default
        else:
            try:
                default = self.parent.Meta.model._meta._forward_fields_map[
                    field_name
                ].default
                if isinstance(default, (str, float, int)):
                    representation["default"] = default
            except:  # TODO Add some explicit exception handling
                pass

        if self.help_text:
            representation["help_text"] = self.help_text

        if self.decorators:
            representation["decorators"] = self.decorators

        if self.extra:
            representation["extra"] = self.extra

        return representation
