import pytest
from rest_framework.exceptions import ValidationError

from bridger.serializers import PrimaryKeyField, PrimaryKeyCharField
from bridger.serializers.fields.types import BridgerType

from ...models import ModelTest


class TestPrimaryKeyField:
    def setup_method(self):
        self.field = PrimaryKeyField()

    def test_not_none(self):
        assert self.field is not None

    def test_field_type(self):
        assert self.field.field_type == BridgerType.PRIMARY_KEY.value

    def test_representation(self):
        assert self.field.get_representation(None, "field_name") == {
            "key": "field_name",
            "label": None,
            "type": self.field.field_type,
            "required": False,
            "read_only": True,
            "decorators": [],
        }


class TestPrimaryKeyCharField:
    def setup_method(self):
        self.field = PrimaryKeyCharField()

    def test_not_none(self):
        assert self.field is not None

    def test_field_type(self):
        assert self.field.field_type == BridgerType.PRIMARY_KEY.value

    def test_representation(self):
        assert self.field.get_representation(None, "field_name") == {
            "key": "field_name",
            "label": None,
            "type": self.field.field_type,
            "required": False,
            "read_only": True,
            "decorators": [],
        }
