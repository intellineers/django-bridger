from bridger import display as dp
from bridger.viewsets import InfiniteDataModelView
from tests.filters import CalendarFilter
from tests.serializers import CalendarModelTestSerializer
from tests.viewsets.model_test import ModelTestModelViewSet


class ModelTestModelCalendarViewSet(ModelTestModelViewSet, InfiniteDataModelView):
    LIST_ENDPOINT = "calendar-list"
    INSTANCE_ENDPOINT = DELETE_ENDPOINT = CREATE_ENDPOINT = "modeltest-list"

    filterset_class = CalendarFilter
    serializer_class = CalendarModelTestSerializer

    LIST_DISPLAY = dp.Calendar(
        title="char_field", start="datetime_field", end="datetime_field1", filter_date_gte="start", filter_date_lte="end",
    )
