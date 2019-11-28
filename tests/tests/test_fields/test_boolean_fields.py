import pytest
from rest_framework.exceptions import ValidationError

from bridger.serializers import BooleanField
from bridger.serializers.fields.types import BridgerType

from ...models import ModelTest


class TestBooleanField:
    def setup_method(self):
        self.field = BooleanField()

    def test_not_none(self):
        assert self.field is not None

    @pytest.mark.parametrize(
        "input, expected",
        [
            (True, True),
            (False, False),
            (1, True),
            (0, False),
            ("1", True),
            ("0", False),
        ],
    )
    def test_to_internal_value(self, input, expected):
        assert self.field.to_internal_value(input) == expected

    @pytest.mark.parametrize("input", ["", [], {}, None])
    def test_to_internal_value_validation_error(self, input):
        with pytest.raises(ValidationError):
            self.field.to_internal_value(input)

    def test_field_type(self):
        assert self.field.field_type == BridgerType.BOOLEAN.value

    def test_representation(self):
        assert self.field.get_representation(None, "field_name") == {
            "key": "field_name",
            "label": None,
            "type": self.field.field_type,
            "required": True,
            "read_only": False,
        }
