from django.urls import include, path
from django.views.generic import TemplateView

from .clubhouse import ClubHouseView
from .frontend_user_configuration import FrontendUserConfigurationModelViewSet
from .markdown.views import AssetCreateView, AssetRetrieveView, BlockDiag, TemplateTagView
from .menus.views import MenuAPIView
from .notifications.viewsets.viewsets import NotificationModelViewSet
from .profile import UserViewSet
from .routers import BridgerRouter
from .share.views import ShareAPIView
from .tags.viewsets import TagRepresentationViewSet
from .views import Config, Profile

router = BridgerRouter()
router.register(
    r"frontenduserconfiguration", FrontendUserConfigurationModelViewSet, basename="frontenduserconfiguration",
)
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
