from django.utils.http import urlencode
from rest_framework.reverse import reverse

from bridger.serializers.fields.related import ListSerializer


class RepresentationSerializerMixin:
    """
    Adds basic functionality for Representation Serializer
    """

    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs["child"] = cls()
        return ListSerializer(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.label_key = kwargs.pop("label_key", self.label_key)
        super().__init__(*args, **kwargs)

    def __new__(cls, *args, **kwargs):
        if "read_only" not in kwargs:
            kwargs["read_only"] = True
        return super().__new__(cls, *args, **kwargs)

    def get_filter_params(self, request):
        if hasattr(self, "filter_params"):
            return self.filter_params
        return None

    def get_representation(self, request, field_name):

        url = reverse(self.endpoint, request=request)

        filter_params = self.get_filter_params(request)
        if filter_params:
            url = f"{url}?{urlencode(filter_params)}"
        representation = {
            "representation_key": field_name,
            "related_key": self.source,
            "endpoint": {"url": url, "value_key": self.value_key, "label_key": self.label_key,},
        }
        if self.help_text:
            representation["help_text"] = self.help_text

        return representation
