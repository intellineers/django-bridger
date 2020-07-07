from bridger.serializers import CharField, IntegerField, Serializer, TextField


class ShareSerializer(Serializer):

    user_id = IntegerField(label="User ID")
    widget_endpoint = CharField(label="Widget URL")
    message = TextField(label="Message", default="Check out this Widget.")
