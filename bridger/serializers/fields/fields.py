from rest_framework import serializers


class AdditionalResourcesField(serializers.ReadOnlyField):
    def get_attribute(self, instance):
        return instance

    def to_representation(self, value):
        method = getattr(self.parent, "get_additional_resources")
        request = self.parent.context["request"]
        return method(value, request, request.user)


class HyperlinkField(serializers.ReadOnlyField):
    def __init__(self, *args, **kwargs):
        self.reverse_name = kwargs.pop("reverse_name")
        super().__init__(*args, **kwargs)

    def get_attribute(self, obj):
        request = self.context.get("request", None)
        if request:
            return reverse(self.reverse_name, args=[obj.id], request=request)
        return reverse(self.reverse_name, args=[obj.id])
