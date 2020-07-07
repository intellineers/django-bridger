from bridger import serializers
from bridger.buttons import WidgetButton
from bridger.enums import WBIcon

from .models import Notification


class NotificationModelSerializer(serializers.ModelSerializer):
    @serializers.register_dynamic_button()
    def notification_buttons(self, instance, request, user):
        btns = instance.buttons or []
        if endpoint := instance.endpoint:
            if "widget_endpoint" in endpoint:
                endpoint = endpoint.split("widget_endpoint=")[1]

            btns.append(WidgetButton(endpoint=endpoint, label="Open", title="Open", icon=WBIcon.DATA.value,))
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
