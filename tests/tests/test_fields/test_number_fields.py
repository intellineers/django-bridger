from decimal import Decimal

import pytest
from rest_framework.exceptions import ValidationError

from bridger.serializers import DecimalField, FloatField, IntegerField
from bridger.serializers.fields.types import BridgerType

from ...models import ModelTest


class TestIntegerField:
    def setup_method(self):
        self.field = IntegerField()

    def test_not_none(self):
        assert self.field is not None

    @pytest.mark.parametrize("input, expected", [(1, 1), ("1", 1), (-1, -1), (0, 0)])
    def test_to_internal_value(self, input, expected):
        assert self.field.to_internal_value(input) == expected

    @pytest.mark.parametrize("input", [None, [], "a", "", {}, 1.2])
    def test_to_internal_value_validation_error(self, input):
        with pytest.raises(ValidationError):
            self.field.to_internal_value(input)

    def test_field_type(self):
        assert self.field.field_type == BridgerType.NUMBER.value

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


class TestDecimalField:
    def setup_method(self):
        self.field = DecimalField(decimal_places=2, max_digits=5)

    def test_not_none(self):
        assert self.field is not None

    @pytest.mark.parametrize(
        "input, expected",
        [(1.0, Decimal(1)), ("1.0", Decimal(1)), (-1.0, Decimal(-1)), (0, Decimal(0))],
    )
    def test_to_internal_value(self, input, expected):
        assert self.field.to_internal_value(input) == expected

    @pytest.mark.parametrize("input", [None, [], "a", "", {}])
    def test_to_internal_value_validation_error(self, input):
        with pytest.raises(ValidationError):
            self.field.to_internal_value(input)

    def test_field_type(self):
        assert self.field.field_type == BridgerType.NUMBER.value

    def test_representation(self):
        assert self.field.get_representation(None, "field_name") == {
            "key": "field_name",
            "label": None,
            "type": self.field.field_type,
            "required": True,
            "read_only": False,
            "precision": 2,
            "decorators": [],
        }

    def test_percent_representation(self):
        _field = self.field
        _field.percent = True
        assert _field.get_representation(None, "field_name") == {
            "key": "field_name",
            "label": None,
            "type": BridgerType.PERCENT.value,
            "required": True,
            "read_only": False,
            "precision": 0,
            "decorators": [],
        }


class TestFloatField:
    def setup_method(self):
        self.field = FloatField()

    def test_not_none(self):
        assert self.field is not None

    @pytest.mark.parametrize(
        "input, expected", [(1.0, 1.0), ("1.0", 1.0), (-1.0, -1.0), (0, 0)]
    )
    def test_to_internal_value(self, input, expected):
        assert self.field.to_internal_value(input) == expected

    @pytest.mark.parametrize("input", [None, [], "a", "", {}])
    def test_to_internal_value_validation_error(self, input):
        with pytest.raises(ValidationError):
            self.field.to_internal_value(input)

    def test_field_type(self):
        assert self.field.field_type == BridgerType.NUMBER.value

    def test_representation(self):
        assert self.field.get_representation(None, "field_name") == {
            "key": "field_name",
            "label": None,
            "type": self.field.field_type,
            "required": True,
            "read_only": False,
            "precision": 2,
            "decorators": [],
        }
