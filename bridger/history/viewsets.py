from django.db.models import F, Value
from django.db.models.functions import Concat
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.reverse import reverse

from bridger import buttons as bt
from bridger import display as dp
from bridger import viewsets
from bridger.enums import Button, RequestType

from .serializers import get_historical_serializer


def get_historical_viewset(model, historical_model):
    class HistoricalModelViewSet(viewsets.ModelViewSet):

        BUTTONS = [Button.REFRESH.value]
        CREATE_BUTTONS = []

        def get_custom_instance_buttons(self, request, buttons):
            return []

        def get_custom_list_instance_buttons(self, request, buttons):
            return []

        LIST_DISPLAY = dp.ListDisplay(
            fields=[
                dp.Field(key="history_date", label="Changed"),
                dp.Field(key="history_change_reason", label="Reason"),
                dp.Field(key="history_type", label="Type"),
                dp.Field(key="user_repr", label="User"),
            ]
        )

        def get_instance_endpoint(self, request, endpoint=None):
            return (
                f"{model.get_endpoint_basename()}-history-list",
                [self.kwargs["model_pk"]],
                {},
            )

        queryset = historical_model.objects.all()
        serializer_class = get_historical_serializer(historical_model)

        ordering_fields = ("history_id",)

        def get_queryset(self):
            qs = super().get_queryset()
            qs = qs.annotate(user_repr=Concat(F("history_user__first_name"), Value(" "), F("history_user__last_name"),))
            return qs

    return HistoricalModelViewSet
