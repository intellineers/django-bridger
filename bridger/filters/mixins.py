class BridgerFilterMixin:
    def __init__(self, *args, **kwargs):
        self.default = kwargs.pop("default", None)
        self.required = kwargs.pop("required", False)
        super().__init__(*args, **kwargs)

    def get_representation(self, request, name):
        self.key = name
        representation = {
            "label": self.label,
            "type": self.filter_type,
            "key": self.field_name,
            "lookup_expr": {self.lookup_expr: self.key},
            "default": {},
        }

        if self.default:
            if callable(self.default):
                representation["default"][self.lookup_expr] = self.default(
                    field=self, request=request
                )
            else:
                representation["default"][self.lookup_expr] = self.default

        if self.required:
            representation["required"] = True
            assert (
                representation["default"] != {}
            ), "If a filter is required, it needs at least one default value"

        return representation
