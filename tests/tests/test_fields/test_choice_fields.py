import pytest
from rest_framework.exceptions import ValidationError

from bridger.serializers import ChoiceField
from bridger.serializers.fields.types import BridgerType

from ...models import ModelTest


class TestChoiceField:
    CHOICES = [
        ("choice1", "Choice 1"),
        ("choice2", "Choice 2"),
    ]

    def setup_method(self):
        self.field = ChoiceField(choices=self.CHOICES)

    def test_not_none(self):
        assert self.field is not None

    @pytest.mark.parametrize("choice", [choice for choice, choice_repr in CHOICES])
    def test_to_internal_value(self, choice):
        assert self.field.to_internal_value(choice) == choice

    @pytest.mark.parametrize("choice", [choice for choice, choice_repr in CHOICES])
    def test_to_representation(self, choice):
        assert self.field.to_representation(choice) == choice

    def test_to_internal_value_validation_error(self):
        with pytest.raises(ValidationError):
            self.field.to_internal_value("choice3")

    def test_field_type(self):
        assert self.field.field_type == BridgerType.SELECT.value

    def test_representation(self):
        choices = [{"label": choice[1], "value": choice[0]} for choice in self.CHOICES]
        assert self.field.get_representation(None, "field_name") == {
            "key": "field_name",
            "label": None,
            "type": self.field.field_type,
            "required": True,
            "read_only": False,
            "choices": choices,
        }
