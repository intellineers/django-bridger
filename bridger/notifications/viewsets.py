from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response

from bridger import display as dp
from bridger import buttons as bt
from bridger import viewsets

from .models import Notification
from .serializers import NotificationModelSerializer


class NotificationModelViewSet(viewsets.ModelViewSet):
    ENDPOINT = "bridger:notification-list"

    INSTANCE_WIDGET_TITLE = "Notification: {{title}}"
    LIST_WIDGET_TITLE = "Notifications"

    LIST_BUTTONS = ["refresh"]
    INSTANCE_BUTTONS = ["refresh", "delete"]
    CREATE_BUTTONS = []

    CUSTOM_BUTTONS = [
        bt.ActionButton(
            method="POST",
            action_label="All notifications read.",
            endpoint="http://localhost:5000/bridger/notification/mark_all_as_read/",
            description_fields="Do you want to mark notifications as read?",
            label="Mark all as read",
            icon="wb-icon-eye-open",
            confirm_label="Yes",
            cancel_label="Cancel",
        ),
        bt.ActionButton(
            method="POST",
            action_label="Delete all read notifications.",
            endpoint="http://localhost:5000/bridger/notification/delete_all_read/",
            description_fields="Do you want delete all read notifications?",
            label="Delete all read notifications",
            icon="wb-icon-trash",
            confirm_label="Yes",
            cancel_label="Cancel",
        ),
    ]

    LIST_DISPLAY = dp.ListDisplay(
        fields=[
            dp.Field(key="title", label="Title"),
            dp.Field(key="timestamp_created", label="Created"),
        ],
        formatting=[
            dp.RowFormatting(
                column="timestamp_read",
                conditions=[
                    dp.RowIconCondition(icon="wb-icon-eye-open", condition=("∃", True)),
                ],
            ),
        ],
    )

    INSTANCE_DISPLAY = dp.InstanceDisplay(
        sections=[dp.Section(fields=dp.FieldSet(fields=["title", "message"]))]
    )

    queryset = Notification.objects.all()
    serializer_class = NotificationModelSerializer

    ordering_fields = ("timestamp_created",)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj.timestamp_read:
            obj.timestamp_read = timezone.now()
            obj.save()
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(recipient=self.request.user)

    @action(methods=["POST"], detail=False)
    def mark_all_as_read(self, request, pk=None):
        Notification.objects.filter(timestamp_read__isnull=True).update(
            timestamp_read=timezone.now()
        )
        return Response({})

    @action(methods=["POST"], detail=False)
    def delete_all_read(self, request, pk=None):
        Notification.objects.filter(timestamp_read__isnull=False).delete()
        return Response({})
