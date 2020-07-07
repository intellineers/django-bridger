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

from .models import Notification
from .serializers import NotificationModelSerializer


class NotificationModelViewSet(viewsets.ModelViewSet):
    ENDPOINT = "bridger:notification-list"

    INSTANCE_TITLE = "Notification: {{title}}"
    LIST_TITLE = "Notifications"

    LIST_BUTTONS = ["refresh"]
    INSTANCE_BUTTONS = ["refresh", "delete"]
    CREATE_BUTTONS = []

    filter_backends = (
        filters.OrderingFilter,
        DjangoFilterBackend,
        filters.SearchFilter,
    )

    def get_custom_buttons(self, request, buttons):
        return [
            bt.ActionButton(
                method=RequestType.POST,
                action_label="All notifications read.",
                endpoint=reverse("bridger:notification-mark-all-as-read", request=request),
                description_fields="Do you want to mark notifications as read?",
                label="Mark all as read",
                icon=WBIcon.EYE.value,
                confirm_config=bt.ButtonConfig(label="Read all"),
                cancel_config=bt.ButtonConfig(label="Cancel"),
                identifiers=["relatedmodeltest-list"],
            ),
            bt.ActionButton(
                method=RequestType.POST,
                action_label="Delete all read notifications.",
                endpoint=reverse("bridger:notification-delete-all-read", request=request),
                description_fields="Do you want delete all read notifications?",
                label="Delete all read notifications",
                icon=WBIcon.TRASH.value,
                confirm_config=bt.ButtonConfig(label="Delete all", level=bt.ButtonLevel.WARNING),
                cancel_config=bt.ButtonConfig(label="Cancel", level=bt.ButtonLevel.ERROR),
                identifiers=[reverse("bridger:notification-list", request=request)],
            ),
        ]

    LIST_DISPLAY = dp.ListDisplay(
        fields=[
            dp.Field(key="title", label="Title"),
            dp.Field(key="timestamp_created", label="Created"),
            dp.Field(key="message", label="Message"),
        ],
        formatting=[
            dp.Formatting(
                column="timestamp_read", formatting_rules=[dp.FormattingRule(icon=WBIcon.EYE.value, condition=("∃", True)),],
            ),
        ],
    )

    INSTANCE_DISPLAY = dp.InstanceDisplay(
        sections=[
            dp.Section(
                fields=dp.FieldSet(
                    fields=[
                        dp.FieldSet(fields=["timestamp_created", "timestamp_received"]),
                        dp.FieldSet(fields=["timestamp_received", "timestamp_mailed"]),
                        "title",
                        "message",
                    ]
                )
            )
        ]
    )

    queryset = Notification.objects.all()
    serializer_class = NotificationModelSerializer

    ordering_fields = ("timestamp_created",)
    ordering = ("-timestamp_created",)
    search_fields = ("title", "message")

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
