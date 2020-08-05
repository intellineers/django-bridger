from bridger import display as dp
from bridger.viewsets import InfiniteDataModelView
from tests.filters import CalendarFilter
from tests.serializers import CalendarModelTestSerializer
from tests.viewsets.model_test import ModelTestModelViewSet

from .display import ModelTestCalendarDisplayConfig

class ModelTestModelCalendarViewSet(ModelTestModelViewSet, InfiniteDataModelView):
    # LIST_ENDPOINT = "calendar-list"
    # INSTANCE_ENDPOINT = DELETE_ENDPOINT = CREATE_ENDPOINT = "modeltest-list"

    filterset_class = CalendarFilter
    serializer_class = CalendarModelTestSerializer

    display_config_class = ModelTestCalendarDisplayConfig
