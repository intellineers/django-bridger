from django.urls import include, path
from rest_framework.routers import DefaultRouter

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
]
