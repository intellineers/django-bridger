from decimal import Decimal

import pytest
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory

from bridger.serializers import AdditionalResourcesField, HyperlinkField


class TestAdditionalResourcesField:
    def setup_method(self):
        self.factory = APIRequestFactory()
        self.field = AdditionalResourcesField()

    def test_not_none(self):
        assert self.field is not None

    @pytest.mark.django_db
    def test_get_attribute(self, model_test):
        assert self.field.get_attribute(model_test) == model_test

    # @pytest.mark.django_db
    # def test_to_representation(self, mocker, model_test):
    #     parent = mocker.patch.object(self.field, "parent")
    #     self.field.to_representation(model_test)

    #     assert parent.get_additional_resources.called


class TestHyperlinkFieldField:
    def setup_method(self):
        self.factory = APIRequestFactory()
        self.field = HyperlinkField(reverse_name="modeltest-list")

    def test_not_none(self):
        assert self.field is not None

    def test_to_representation(self):
        assert self.field.to_representation("abc") == "abc"

    @pytest.mark.django_db
    def test_get_attribute_with_request(self, mocker, model_test):
        self.field._context = {"request": self.factory.get("/")}
        attr = self.field.get_attribute(model_test)
        assert attr is not None and attr != ""

    @pytest.mark.django_db
    def test_get_attribute(self, mocker, model_test):
        attr = self.field.get_attribute(model_test)
        assert attr is not None and attr != ""
