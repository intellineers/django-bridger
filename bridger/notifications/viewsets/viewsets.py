from django.utils import timezone
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.reverse import reverse

from bridger import buttons as bt
from bridger import display as dp
from bridger import viewsets
from bridger.enums import RequestType, WBIcon
from bridger.filters import DjangoFilterBackend

from bridger.notifications.models import Notification
from bridger.notifications.serializers import NotificationModelSerializer

from .buttons import NotificationButtonConfig
from .display import NotificationDisplayConfig
from .endpoint import NotificationEndpointConfig
from .title import NotificationTitleConfig

class NotificationModelViewSet(viewsets.ModelViewSet):

    queryset = Notification.objects.all()
    serializer_class = NotificationModelSerializer
    filter_backends = (
        filters.OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter,
    )

    ordering_fields = ("timestamp_created",)
    ordering = ("-timestamp_created",)
    search_fields = ("title", "message")

    title_config_class = NotificationTitleConfig
    display_config_class = NotificationDisplayConfig
    endpoint_config_class = NotificationEndpointConfig
    button_config_class = NotificationButtonConfig

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj.timestamp_read:
            obj.timestamp_read = timezone.now()
            obj.save()
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.get_queryset().filter(timestamp_received__isnull=True).update(timestamp_received=timezone.now())
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(recipient=self.request.user)

    @action(methods=["POST"], detail=False)
    def mark_all_as_read(self, request, pk=None):
        Notification.objects.filter(timestamp_read__isnull=True).update(timestamp_read=timezone.now())
        return Response({})

    @action(methods=["POST"], detail=False)
    def delete_all_read(self, request, pk=None):
        Notification.objects.filter(timestamp_read__isnull=False).delete()
        return Response({})
