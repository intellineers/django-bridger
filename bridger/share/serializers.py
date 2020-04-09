from bridger.notifications.models import Notification, NotificationSendType
from bridger.serializers import Serializer, CharField, IntegerField, TextField


class ShareSerializer(Serializer):

    user_id = IntegerField(label="User ID")
    widget_endpoint = CharField(label="Widget URL")
    message = TextField(label="Message", default="Check out this Widget.")

