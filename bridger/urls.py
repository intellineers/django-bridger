from django.urls import include, path
from django.views.generic import TemplateView

from .frontend_user_configuration import FrontendUserConfigurationModelViewSet
from .notifications.viewsets import NotificationModelViewSet
from .routers import BridgerRouter
from .views import Config, Profile

from .share.views import ShareAPIView
from .menus.views import MenuAPIView
from .profile import UserViewSet
from .markdown.views import BlockDiag
from .clubhouse import ClubHouseView

# fmt: off
router = BridgerRouter()
router.register(r"frontenduserconfiguration", FrontendUserConfigurationModelViewSet, basename="frontenduserconfiguration")
router.register(r"notification", NotificationModelViewSet, basename="notification")
router.register(r"user", UserViewSet, basename="user")
router.register(r"clubhouse", ClubHouseView, basename="clubhouse")
# fmt: on

urlpatterns = [
    path("config/", Config.as_view(), name="config"),
    path("profile/", Profile.as_view(), name="profile"),
    path("menu/", MenuAPIView.as_view(), name="menu"),
    path("share/", ShareAPIView.as_view(), name="share"),
    path("markdown/blockdiag/", BlockDiag.as_view(), name="blockdiag"),
    path("", include(router.urls)),
]
