from django.urls import include, path

from .frontend_user_configuration import FrontendUserConfigurationModelViewSet
from .routers import BridgerRouter
from .views import Config, Menu, Profile

# fmt: off
router = BridgerRouter()
router.register(r"frontenduserconfiguration", FrontendUserConfigurationModelViewSet, basename="frontenduserconfiguration")
# fmt: on

urlpatterns = [
    path("config/", Config.as_view(), name="config"),
    path("profile/", Profile.as_view(), name="profile"),
    path("menu/", Menu.as_view(), name="menu"),
    path("", include(router.urls)),
]
