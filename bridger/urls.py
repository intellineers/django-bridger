from django.urls import include, path
from django.views.generic import TemplateView

from .frontend_user_configuration import FrontendUserConfigurationModelViewSet
from .notifications.viewsets import NotificationModelViewSet
from .routers import BridgerRouter
from .views import Config, Profile

from .share.views import ShareAPIView
from .menus.views import MenuAPIView
from .profile import UserViewSet

# fmt: off
router = BridgerRouter()
router.register(r"frontenduserconfiguration", FrontendUserConfigurationModelViewSet, basename="frontenduserconfiguration")
router.register(r"notification", NotificationModelViewSet, basename="notification")
router.register(r"user", UserViewSet, basename="user")
# fmt: on

urlpatterns = [
    path("config/", Config.as_view(), name="config"),
    path("profile/", Profile.as_view(), name="profile"),
    path("menu/", MenuAPIView.as_view(), name="menu"),
    path("share/", ShareAPIView.as_view(), name="share"),
    path("", include(router.urls)),
]
