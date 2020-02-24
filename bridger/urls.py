from django.urls import include, path

from .frontend_user_configuration import FrontendUserConfigurationModelViewSet
from .routers import BridgerRouter
from .views import Config, Menu, Profile
from django.views.generic import TemplateView

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


def bundled_frontend(url):
    return path(f"{url}", TemplateView.as_view(template_name="bridger/frontend.html"))
