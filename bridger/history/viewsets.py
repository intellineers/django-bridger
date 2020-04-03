from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.reverse import reverse

from bridger import buttons as bt
from bridger import display as dp
from bridger import viewsets
from bridger.enums import RequestType

from .serializers import get_historical_serializer
from bridger.enums import Button


def get_historical_viewset(model, historical_model):
    class HistoricalModelViewSet(viewsets.ModelViewSet):

        BUTTONS = [Button.REFRESH.value]
        CREATE_BUTTONS = []

        LIST_DISPLAY = dp.ListDisplay(
            fields=[
                dp.Field(key="history_date", label="Changed"),
                dp.Field(key="history_change_reason", label="Reason"),
                dp.Field(key="history_type", label="Type"),
            ]
        )

        # INSTANCE_ENDPOINT = model.get_endpoint()

        queryset = historical_model.objects.all()
        serializer_class = get_historical_serializer(historical_model)

        ordering_fields = ("history_id",)

    return HistoricalModelViewSet

