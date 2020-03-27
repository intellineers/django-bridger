from bridger.buttons import WidgetButton
from bridger import serializers

from .models import Notification


class NotificationModelSerializer(serializers.ModelSerializer):

    @serializers.register_dynamic_button()
    def notification_buttons(self, instance, request, user):
        btns = instance.buttons or []
        if instance.endpoint:
            btns.append(WidgetButton(
                endpoint=instance.endpoint,
                label="Open",
                title="Open",
                icon="wb-icon-data"
            ))
        return btns

    class Meta:
        model = Notification
        fields = read_only_fields = (
            "id",
            "recipient",
            "title",
            "message",
            "timestamp_created",
            "timestamp_received",
            "timestamp_read",
            "timestamp_mailed",
            "_buttons",
        )
