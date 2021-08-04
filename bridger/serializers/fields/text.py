from rest_framework import serializers
from rest_framework.reverse import reverse

from .mixins import BridgerSerializerFieldMixin
from .types import BridgerType, ReturnContentType


class CharField(BridgerSerializerFieldMixin, serializers.CharField):
    field_type = BridgerType.TEXT.value

    def __init__(self, *args, **kwargs):
        self.secure = kwargs.pop("secure", False)
        super().__init__(*args, **kwargs)

    def get_representation(self, request, field_name):
        representation = super().get_representation(request, field_name)
        if self.secure:
            representation["secure"] = True
        return representation


class StringRelatedField(BridgerSerializerFieldMixin, serializers.StringRelatedField):
    field_type = BridgerType.TEXT.value


class TextField(CharField):
    field_type = BridgerType.TEXTEDITOR.value
    texteditor_content_type = ReturnContentType.HTML.value

    def __init__(self, *args, **kwargs):
        """The constructor method.
        This pops the 'plugin_configs' dict from the kwargs and calls the
        parents init method.

        Parameters
        ----------
        plugin_configs : dict, optional
            A dictionary that contains a dictionary for each plugin of the
            texteditor. The configuration for each plugin must be available
            under a unique key.
        """
        self.plugin_configs = kwargs.pop('plugin_configs', None)
        super().__init__(*args, **kwargs)

    def get_representation(self, request, field_name):
        representation = super().get_representation(request, field_name)
        representation["content_type"] = self.texteditor_content_type
        if not self.plugin_configs:
            representation["plugin_configs"] = {}
        else:
            representation["plugin_configs"] = self.plugin_configs(request)
        return representation


class MarkdownTextField(TextField):
    field_type = BridgerType.MARKDOWNEDITOR.value
    texteditor_content_type = ReturnContentType.MARKDOWN.value

    def __init__(self, metadata_field=None, *args, **kwargs):
        self.metadata_field = metadata_field
        super().__init__(*args, **kwargs)

    def get_representation(self, request, field_name):
        representation = super().get_representation(request, field_name)
        representation["image_upload"] = reverse("bridger:markdown-asset-upload", request=request)
        representation["tags"] = reverse("bridger:markdown-tags", request=request)
        if self.metadata_field:
            representation["metadata_field"] = self.metadata_field
        return representation
