from bridger.buttons import WidgetButton
from bridger import serializers


def get_historical_serializer(historical_model):
    class HistoricalModelSerializer(serializers.ModelSerializer):
        # user_repr = serializers.CharField()

        class Meta:
            model = historical_model
            fields = read_only_fields = (
                "history_id",
                "history_date",
                "history_change_reason",
                "history_type",
                "history_user",
                # "user_repr",
            )

    return HistoricalModelSerializer
