class BridgerFilterMixin:
    def __init__(self, *args, **kwargs):
        self.default = kwargs.pop("default", None)
        super().__init__(*args, **kwargs)

    def get_representation(self, request, name):
        self.key = name
        representation = {
            "label": self.label,
            "type": self.filter_type,
            "key": self.field_name,
            "lookup_expr": {self.lookup_expr: self.key},
        }

        if self.default:
            representation["default"] = self.default

        return representation
