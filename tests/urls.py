from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, reverse_lazy, path, re_path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.views.generic import RedirectView
from bridger.frontend import FrontendView
from bridger.routers import BridgerRouter

from .viewsets import (
    ModelTestChartViewSet,
    ModelTestModelCalendarViewSet,
    ModelTestModelViewSet,
    ModelTestRepresentationViewSet,
    MyPandasView,
    RelatedModelTestModelViewSet,
    RelatedModelTestRepresentationViewSet,
)

# fmt: off
router = BridgerRouter()
router.register(r"modeltest", ModelTestModelViewSet, basename="modeltest")
router.register(r"modeltestrepresentation", ModelTestRepresentationViewSet, basename="modeltestrepresentation")
router.register(r"relatedmodeltest", RelatedModelTestModelViewSet, basename="relatedmodeltest")
router.register(r"relatedmodeltestrepresentation", RelatedModelTestRepresentationViewSet, basename="relatedmodeltestrepresentation")
router.register(r"calendar", ModelTestModelCalendarViewSet, basename="calendar")
router.register(r"modelchart", ModelTestChartViewSet, basename="modelchart")
# fmt: on

urlpatterns = [
    path("", include(router.urls)),
    # path("bundle/", TemplateView.as_view(template_name="bundled_index.html")),
    path("admin/", admin.site.urls),
    path("bridger/", include(("bridger.urls", "bridger"), namespace="bridger")),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("pandas/", MyPandasView.as_view(), name="pandas_view"),
    FrontendView.bundled_view(""),
    path('', RedirectView.as_view(url=reverse_lazy('frontend')))
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
