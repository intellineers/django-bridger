from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import Config, Menu, Profile
from .frontend_user_configuration import FrontendUserConfigurationModelViewSet

# fmt: off
router = DefaultRouter()
router.register(r"frontenduserconfiguration", FrontendUserConfigurationModelViewSet, basename="frontenduserconfiguration")
# fmt: on

urlpatterns = [
    path("config/", Config.as_view(), name="config"),
    path("profile/", Profile.as_view(), name="profile"),
    path("menu/", Menu.as_view(), name="menu"),
    path("", include(router.urls)),
]
