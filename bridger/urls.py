from django.urls import include, path
from django.views.generic import TemplateView

from .frontend_user_configuration import FrontendUserConfigurationModelViewSet
from .notifications.viewsets import NotificationModelViewSet
from .tags.viewsets import TagRepresentationViewSet
from .routers import BridgerRouter
from .views import Config, Profile

from .share.views import ShareAPIView
from .menus.views import MenuAPIView
from .profile import UserViewSet
from .markdown.views import (
    BlockDiag,
    AssetCreateView,
    AssetRetrieveView,
    TemplateTagView,
)
from .clubhouse import ClubHouseView

router = BridgerRouter()
router.register(r"frontenduserconfiguration", FrontendUserConfigurationModelViewSet, basename="frontenduserconfiguration")
router.register(r"notification", NotificationModelViewSet, basename="notification")
router.register(r"user", UserViewSet, basename="user")
router.register(r"clubhouse", ClubHouseView, basename="clubhouse")
router.register(r"tagrepresentation", TagRepresentationViewSet, basename="tagrepresentation")

urlpatterns = [
    path("config/", Config.as_view(), name="config"),
    path("profile/", Profile.as_view(), name="profile"),
    path("menu/", MenuAPIView.as_view(), name="menu"),
    path("share/", ShareAPIView.as_view(), name="share"),
    path("markdown/blockdiag/", BlockDiag.as_view(), name="blockdiag"),
    path("markdown/asset/", AssetCreateView.as_view(), name="markdown-asset-upload"),
    path("markdown/asset/<uuid>/", AssetRetrieveView.as_view(), name="asset-retrieve"),
    path("markdown/templatetag/", TemplateTagView.as_view(), name="markdown-tags"),
    path("", include(router.urls)),
]
