from decimal import Decimal

import pytest
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse
from bridger.serializers import AdditionalResourcesField, HyperlinkField

from ...models import ModelTest


class TestAdditionalResourcesField:
    def setup_method(self):
        self.factory = APIRequestFactory()
        self.field = AdditionalResourcesField()

    def test_not_none(self):
        assert self.field is not None

    @pytest.mark.django_db
    def test_get_attribute(self):
        instance = ModelTest.get_random_instance()
        assert self.field.get_attribute(instance) == instance

    @pytest.mark.django_db
    def test_to_representation(self, mocker):
        instance = ModelTest.get_random_instance()
        parent = mocker.patch.object(self.field, "parent")
        self.field.to_representation(instance)

        assert parent.get_additional_resources.called


class TestHyperlinkFieldField:
    def setup_method(self):
        self.factory = APIRequestFactory()
        self.field = HyperlinkField(reverse_name="test")

    def test_not_none(self):
        assert self.field is not None

    def test_to_representation(self):
        assert self.field.to_representation("abc") == "abc"

    @pytest.mark.django_db
    def test_get_attribute_with_request(self, mocker):
        self.field._context = {"request": self.factory.get("/")}
        instance = ModelTest.get_random_instance()
        attr = self.field.get_attribute(instance)
        assert attr is not None and attr != ""

    @pytest.mark.django_db
    def test_get_attribute(self, mocker):
        instance = ModelTest.get_random_instance()
        attr = self.field.get_attribute(instance)
        assert attr is not None and attr != ""
