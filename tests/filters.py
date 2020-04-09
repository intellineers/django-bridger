from django.db.models import Q
from bridger.filters import (
    BooleanFilter,
    CharFilter,
    DateFilter,
    FilterSet,
)
from bridger.filters.defaults import (
    current_quarter_date_start,
    current_quarter_date_end,
    current_month_date_start,
    current_month_date_end,
)

from .models import ModelTest, RelatedModelTest


class PandasFilterSet(FilterSet):
    char_field = CharFilter(label="Char")

    class Meta:
        model = ModelTest
        fields = ["char_field"]


class ModelTestFilterSet(FilterSet):

    before_2k = BooleanFilter(label="Before 2k", method="filter_2k")

    datetime_field = DateFilter(
        label="DateTime", lookup_expr="exact", field_name="datetime_field",
    )

    def filter_some_date(self, queryset, name, value):
        return queryset

    def filter_2k(self, queryset, name, value):
        if value:
            return queryset.filter(date_field__year__lt=2000)
        return queryset

    class Meta:
        model = ModelTest
        fields = {
            "integer_field": ["lte", "gte", "lt", "gt", "exact"],
            "char_field": ["exact", "icontains"],
            "datetime_field": ["lte", "gte"],
            "date_field": ["exact"],
            "status_field": ["exact"],
            "decimal_field": ["lte", "gte", "lt", "gt", "exact"],
            "before_2k": ["exact", "icontains"],
            "related_models": ["exact"],
        }


class RelatedModelTestFilterSet(FilterSet):
    # char_field = CharFilter(lookup_expr="icontains")

    class Meta:
        model = RelatedModelTest
        # fields = ["char_field", "model_test"]
        fields = {"char_field": ["exact", "icontains"], "model_test": ["exact"]}


class CalendarFilter(FilterSet):

    start = DateFilter(
        label="Date", lookup_expr="gte", field_name="date_field", method="start_filter",
    )
    end = DateFilter(
        label="Date", lookup_expr="lte", field_name="date_field", method="end_filter",
    )

    def start_filter(self, queryset, name, value):
        return queryset.filter(
            Q(datetime_field__date__gte=value) & Q(datetime_field1__date__gte=value)
        )

    def end_filter(self, queryset, name, value):
        return queryset.filter(
            Q(datetime_field__date__lte=value) & Q(datetime_field1__date__lte=value)
        )

    class Meta:
        model = ModelTest
        fields = ["start", "end"]
