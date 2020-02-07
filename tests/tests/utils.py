import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, force_authenticate


@pytest.mark.django_db
class AuthenticatedTest:
    def setup_method(self):
        self.superuser = get_user_model().objects.create(
            username="test_user", password="ABC", is_active=True, is_superuser=True
        )
        self.factory = APIRequestFactory()
        self.blank_get_request = self.factory.get("")
        self.blank_options_request = self.factory.options("")
        force_authenticate(self.blank_get_request, self.superuser)
        force_authenticate(self.blank_options_request, self.superuser)

        self.blank_unauthenticated_get_request = self.factory.get("")
