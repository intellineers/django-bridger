import pytest
from rest_framework.exceptions import ValidationError

from bridger.serializers import JSONTextEditorField
from bridger.serializers.fields.types import BridgerType, ReturnContentType

from ...models import ModelTest


class TestJSONTextEditorField:
    def setup_method(self):
        self.field = JSONTextEditorField()

    def test_not_none(self):
        assert self.field is not None

    def test_field_type(self):
        assert self.field.field_type == BridgerType.TEXTEDITOR.value

    def test_representation(self):
        assert self.field.get_representation(None, "field_name") == {
            "key": "field_name",
            "content_type": ReturnContentType.JSON.value,
            "label": None,
            "type": self.field.field_type,
            "required": True,
            "read_only": False,
        }
