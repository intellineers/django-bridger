from bridger.filters import FilterSet, DateFilter, DefaultDateRangeFilterValues
from .models import ModelTest


class ModelTestFilterSet(FilterSet):
    date_lte = DateFilter(
        label="Date",
        lookup_expr="lte",
        field_name="date_field",
        date_range=True,
        visible=True,
        # default=DefaultDateRangeFilterValues.CURRENT_QUARTER_END,
    )
    date_gte = DateFilter(
        label="Date",
        lookup_expr="gte",
        field_name="date_field",
        date_range=True,
        visible=True,
        # default=DefaultDateRangeFilterValues.CURRENT_QUARTER_START,
    )

    class Meta:
        model = ModelTest
        fields = ["char_field", "date_lte", "date_gte"]
