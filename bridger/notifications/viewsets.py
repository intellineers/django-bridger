from django.utils import timezone

from bridger import display as dp
from bridger import viewsets

from .models import Notification
from .serializers import NotificationModelSerializer


class ModelTestModelViewSet(viewsets.ModelViewSet):
    ENDPOINT = "bridger:notification-list"

    INSTANCE_WIDGET_TITLE = "Notification: {{title}}"
    LIST_WIDGET_TITLE = "Notifications"

    LIST_DISPLAY = dp.ListDisplay(
        fields=[
            dp.Field(key="title", label="Title"),
            dp.Field(key="timestamp_created", label="Created"),
        ],
    )

    INSTANCE_DISPLAY = dp.InstanceDisplay(
        sections=[dp.Section(fields=dp.FieldSet(fields=["title", "message"]))]
    )

    queryset = Notification.objects.all()
    serializer_class = NotificationModelSerializer

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj.timestamp_read:
            obj.timestamp_read = timezone.now()
            obj.save()
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(recipient=self.request.user)
