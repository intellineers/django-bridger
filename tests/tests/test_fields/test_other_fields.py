import pytest
from rest_framework.exceptions import ValidationError

from bridger.serializers import RangeSelectField, StarRatingField
from bridger.serializers.fields.types import BridgerType

from ...models import ModelTest


class TestStarRatingField:
    def setup_method(self):
        self.field = StarRatingField()

    def test_not_none(self):
        assert self.field is not None

    def test_field_type(self):
        assert self.field.field_type == "starrating"

    def test_representation(self):
        assert self.field.get_representation(None, "field_name") == {
            "key": "field_name",
            "label": None,
            "type": self.field.field_type,
            "required": True,
            "read_only": False,
            "precision": 0,
            "decorators": [],
        }


class TestRangeSelectField:
    def setup_method(self):
        self.field = RangeSelectField()

    def test_not_none(self):
        assert self.field is not None

    def test_field_type(self):
        assert self.field.field_type == "rangeselect"

    def test_representation(self):
        assert self.field.get_representation(None, "field_name") == {
            "key": "field_name",
            "label": None,
            "type": self.field.field_type,
            "required": True,
            "read_only": False,
            "color": self.field.color,
            "decorators": [],
        }
