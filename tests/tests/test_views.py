import pytest
from django.test import override_settings

from bridger.menus import default_registry
from bridger.menus.views import MenuAPIView
from bridger.views import Config, Profile

from .utils import AuthenticatedTest

# # TODO: Make proper Test
# class TestMenu(AuthenticatedTest):
#     def test_menu(self):
#         menu = MenuAPIView.as_view()
#         response = menu(self.blank_get_request)

#         assert response.data == default_registry.to_dict(self.blank_get_request)

#     @override_settings(
#         BRIDGER_SETTINGS={"DEFAULT_AUTH_CONFIG": "bridger.auth.unauthenticated"}
#     )
#     def test_unauthenticated_menu(self):
#         menu = MenuAPIView.as_view()
#         response = menu(self.blank_unauthenticated_get_request)

#         assert response.data == default_registry.to_dict(self.blank_get_request)


# TODO: Make proper Test
class TestProfile(AuthenticatedTest):
    def test_config(self):
        profile = Profile.as_view()
        response = profile(self.blank_get_request)
        assert response


# TODO: Make proper Test
class TestConfig(AuthenticatedTest):
    def test_config(self):
        config = Config.as_view()
        response = config(self.blank_get_request)
        assert response
