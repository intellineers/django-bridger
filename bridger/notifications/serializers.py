from bridger import serializers

from .models import Notification


class NotificationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = read_only_fields = (
            "id",
            "recipient",
            "title",
            "message",
            "buttons",
            "timestamp_created",
            "timestamp_received",
            "timestamp_read",
            "timestamp_mailed",
        )
