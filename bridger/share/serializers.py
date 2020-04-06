from bridger.serializers import Serializer, CharField, IntegerField


class ShareSerializer(Serializer):

    user_id = IntegerField(label="User ID")
    widget_endpoint = CharField(label="Widget URL")

