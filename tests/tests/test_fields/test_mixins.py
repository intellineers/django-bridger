import pytest
from rest_framework.exceptions import ValidationError
from rest_framework.fields import Field

from bridger.serializers.fields.mixins import BridgerSerializerFieldMixin

from ...models import ModelTest


class TestListField:
    def setup_method(self):
        class TestSubClass(BridgerSerializerFieldMixin, Field):
            field_type = "field_type"

        self.TestSubClass = TestSubClass

    def test_init(self):
        test_sub_class_instance = self.TestSubClass()
        assert test_sub_class_instance is not None

    def test_init_with_extra(self):
        test_sub_class_instance = self.TestSubClass(extra={})
        assert test_sub_class_instance is not None

    def test_init_with_decorators(self):
        test_sub_class_instance = self.TestSubClass(decorators={})
        assert test_sub_class_instance is not None

    @pytest.mark.parametrize("label", ["", "Label", None])
    @pytest.mark.parametrize("required", [True, False])
    @pytest.mark.parametrize("read_only", [False])
    def test_get_representation(self, label, required, read_only):
        test_sub_class_instance = self.TestSubClass(label=label, required=required, read_only=read_only,)
        assert test_sub_class_instance.get_representation(None, "field_name") == {
            "key": "field_name",
            "label": label,
            "type": "field_type",
            "required": required,
            "read_only": read_only,
            "decorators": [],
        }

    def test_get_representation_additional_attrs(self):
        help_text = "This is a help text"
        decorators = {"some_field": [{"position": "right", "value": "%"}]}
        extra = {"some_key": "some_value"}

        test_sub_class_instance = self.TestSubClass(help_text=help_text, decorators=decorators, extra=extra,)
        assert test_sub_class_instance.get_representation(None, "field_name") == {
            "key": "field_name",
            "label": None,
            "type": "field_type",
            "required": True,
            "read_only": False,
            "help_text": help_text,
            "decorators": decorators,
            "extra": extra,
        }

    def test_get_representation_additional_default_value(self):
        default_value = 100
        test_sub_class_instance = self.TestSubClass(default=default_value)

        assert test_sub_class_instance.get_representation(None, "field_name") == {
            "key": "field_name",
            "label": None,
            "type": "field_type",
            "required": False,  # If a default is given, then it cannot be required
            "read_only": False,
            "default": default_value,
            "decorators": [],
        }

    def test_get_representation_additional_default_method(self):
        def default_method():
            return 100

        test_sub_class_instance = self.TestSubClass(default=default_method)

        assert test_sub_class_instance.get_representation(None, "field_name") == {
            "key": "field_name",
            "label": None,
            "type": "field_type",
            "required": False,  # If a default is given, then it cannot be required
            "read_only": False,
            "default": default_method(),
            "decorators": [],
        }
