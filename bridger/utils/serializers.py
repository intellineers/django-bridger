import bridger.serializers as wb_serializers
from bridger.utils.date import current_quarter_date_start, current_quarter_date_end

class StartEndDateSerializer(wb_serializers.Serializer):
    start = wb_serializers.DateField(label="Start", default=current_quarter_date_start)
    end = wb_serializers.DateField(label="End", default=current_quarter_date_end)