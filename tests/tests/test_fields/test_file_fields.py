import pytest
from rest_framework.exceptions import ValidationError

from bridger.serializers import FileField, ImageField
from bridger.serializers.fields.types import BridgerType

from ...models import ModelTest


class TestImageField:
    def setup_method(self):
        self.field = ImageField()

    def test_not_none(self):
        assert self.field is not None

    def test_field_type(self):
        assert self.field.field_type == BridgerType.IMAGE.value

    def test_representation(self):
        assert self.field.get_representation(None, "field_name") == {
            "key": "field_name",
            "label": None,
            "type": self.field.field_type,
            "required": True,
            "read_only": False,
        }


class TestFileField:
    def setup_method(self):
        self.field = FileField()

    def test_not_none(self):
        assert self.field is not None

    def test_field_type(self):
        assert self.field.field_type == BridgerType.FILE.value

    def test_representation(self):
        assert self.field.get_representation(None, "field_name") == {
            "key": "field_name",
            "label": None,
            "type": self.field.field_type,
            "required": True,
            "read_only": False,
        }
