from bridger import serializers
from bridger.buttons import WidgetButton


def get_historical_serializer(historical_model):
    class HistoricalModelSerializer(serializers.ModelSerializer):
        user_repr = serializers.SerializerMethodField()

        def get_user_repr(self, obj):
            user = obj.history_user
            return f"{user.first_name} {user.last_name}"

        class Meta:
            model = historical_model
            fields = read_only_fields = (
                "history_id",
                "history_date",
                "history_change_reason",
                "history_type",
                "history_user",
                "user_repr",
            )

    return HistoricalModelSerializer
