from bridger.filters import (
    BooleanFilter,
    FilterSet,
    DateFilter,
    DefaultDateRangeFilterValues,
)
from .models import ModelTest


class ModelTestFilterSet(FilterSet):
    before_2k = BooleanFilter(label="Before 2k", method="filter_2k")
    date_lte = DateFilter(
        label="Date", lookup_expr="lte", field_name="date_field", date_range=True,
    )
    date_gte = DateFilter(
        label="Date", lookup_expr="gte", field_name="date_field", date_range=True,
    )

    def filter_2k(self, queryset, name, value):
        if value:
            return queryset.filter(date_field__year__lt=2000)
        return queryset

    class Meta:
        model = ModelTest
        fields = ["char_field", "date_lte", "date_gte", "before_2k"]
