import pytest
from rest_framework.exceptions import ValidationError

from bridger.serializers import CharField, StringRelatedField, TextField
from bridger.serializers.fields.types import BridgerType

from ...models import ModelTest


class TestCharField:
    def setup_method(self):
        self.field = CharField()

    def test_not_none(self):
        assert self.field is not None

    @pytest.mark.parametrize("input, expected", [(1, "1"), ("a", "a")])
    def test_to_internal_value(self, input, expected):
        assert self.field.to_internal_value(input) == expected

    def test_to_internal_value_validation_error(self):
        with pytest.raises(ValidationError):
            self.field.to_internal_value(None)

    def test_field_type(self):
        assert self.field.field_type == BridgerType.TEXT.value

    def test_representation(self):
        assert self.field.get_representation(None, "field_name") == {
            "key": "field_name",
            "label": None,
            "type": self.field.field_type,
            "required": True,
            "read_only": False,
        }


@pytest.mark.django_db
class TestStringRelatedField:
    def setup_method(self):
        self.field = StringRelatedField()
        self.instance = ModelTest.get_random_instance()

    def test_not_none(self):
        assert self.field is not None

    def test_to_representation(self):
        assert self.field.to_representation(self.instance) == str(self.instance)

    def test_field_type(self):
        assert self.field.field_type == BridgerType.TEXT.value

    def test_representation(self):
        assert self.field.get_representation(None, "field_name") == {
            "key": "field_name",
            "label": None,
            "type": self.field.field_type,
            "required": False,
            "read_only": True,
        }


class TestTextField:
    def setup_method(self):
        self.field = TextField()

    def test_not_none(self):
        assert self.field is not None

    @pytest.mark.parametrize("input, expected", [(123, "123"), ("abc", "abc")])
    def test_to_internal_value(self, input, expected):
        assert self.field.to_internal_value(input) == expected

    def test_to_internal_value_validation_error(self):
        with pytest.raises(ValidationError):
            self.field.to_internal_value(None)

    def test_field_type(self):
        assert self.field.field_type == BridgerType.TEXTEDITOR.value

    def test_representation(self):
        assert self.field.get_representation(None, "field_name") == {
            "key": "field_name",
            "content_type": self.field.texteditor_content_type,
            "label": None,
            "type": self.field.field_type,
            "required": True,
            "read_only": False,
        }
