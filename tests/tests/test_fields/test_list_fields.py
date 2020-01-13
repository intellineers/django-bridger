import pytest
from rest_framework.exceptions import ValidationError

from bridger.serializers import ListField
from bridger.serializers.fields.types import BridgerType

from ...models import ModelTest


class TestListField:
    def setup_method(self):
        self.field = ListField()

    def test_not_none(self):
        assert self.field is not None

    def test_field_type(self):
        assert self.field.field_type == BridgerType.LIST.value

    def test_representation(self):
        assert self.field.get_representation(None, "field_name") == {
            "key": "field_name",
            "label": None,
            "type": self.field.field_type,
            "required": True,
            "read_only": False,
            "decorators": [],
        }
