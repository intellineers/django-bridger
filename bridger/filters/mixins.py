class BridgerFilterMixin:
    def __init__(self, *args, **kwargs):
        self.default = kwargs.pop("default", None)
        self.visible = kwargs.pop("visible", False)
        self.required = kwargs.pop("required", False)
        super().__init__(*args, **kwargs)

    def get_representation(self, request, name):
        self.key = name
        representation = {
            "label": self.label,
            "type": self.filter_type,
            "key": name,
            "visible": self.visible,
            "required": self.required,
        }

        if self.default:
            representation["default"] = self.default

        return representation
