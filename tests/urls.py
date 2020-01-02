from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .viewsets import (
    ModelTestModelViewSet,
    ModelTestRepresentationViewSet,
    RelatedModelTestModelViewSet,
)

# fmt: off
router = DefaultRouter()
router.register(r"modeltest", ModelTestModelViewSet, basename="modeltest")
router.register(r"modeltestrepresentation", ModelTestRepresentationViewSet, basename="modeltestrepresentation")
router.register(r"relatedmodeltest", RelatedModelTestModelViewSet, basename="relatedmodeltest")
# fmt: on

urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
    path("bridger/", include(("bridger.urls", "bridger"), namespace="bridger")),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
