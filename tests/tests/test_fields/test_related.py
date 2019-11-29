import pytest
from rest_framework.exceptions import ValidationError
from rest_framework.fields import Field

from bridger.serializers import PrimaryKeyRelatedField
from bridger.serializers.fields.mixins import BridgerSerializerFieldMixin
from bridger.serializers.fields.related import BridgerManyRelatedField
from bridger.serializers.fields.types import BridgerType, ReturnContentType

from ...models import ModelTest


class TestBridgerManyRelatedField:
    def setup_method(self):
        class TestSubClass(BridgerSerializerFieldMixin, Field):
            field_type = "field_type"

        self.TestSubClass = TestSubClass
        self.field = BridgerManyRelatedField

    def test_not_none(self):
        assert self.field(child_relation=self.TestSubClass()) is not None

    def test_required_allowed_null(self):
        field = self.field(child_relation=self.TestSubClass(), required=False)
        assert field.allow_null

    def test_validation_allow_null(self):
        field = self.field(child_relation=self.TestSubClass(), required=False)
        validated_data = field.run_validation(None)

        assert validated_data == []

    def test_get_representation(self):
        field = self.field(child_relation=self.TestSubClass())
        assert field.get_representation(None, "field_name")["multiple"]


class TestPrimaryKeyRelatedField:
    def setup_method(self):
        self.field = PrimaryKeyRelatedField

    def test_is_not_none_read_only(self):
        assert self.field(read_only=True) is not None

    def test_is_not_none_queryset(self):
        assert self.field(queryset=ModelTest.objects.all()) is not None

    def test_many_is_not_none(self):
        field = self.field.many_init(required=True, queryset=ModelTest.objects.all())
        assert field is not None
        assert isinstance(field, BridgerManyRelatedField)

    def test_get_representation(self):
        assert self.field(queryset=ModelTest.objects.all()).get_representation(
            None, "field_name"
        ) == {
            "key": "field_name",
            "label": None,
            "type": BridgerType.SELECT.value,
            "required": True,
            "read_only": False,
        }

    def test_get_representation_multiple(self):
        assert self.field.many_init(
            queryset=ModelTest.objects.all()
        ).get_representation(None, "field_name") == {
            "key": "field_name",
            "label": "",
            "type": BridgerType.SELECT.value,
            "required": True,
            "read_only": False,
            "multiple": True,
        }

    @pytest.mark.django_db
    def test_run_validation(self):
        instance = ModelTest.get_random_instance()
        validated_data = self.field(
            required=False, queryset=ModelTest.objects.all()
        ).run_validation(data=instance.pk)
        assert validated_data == instance

