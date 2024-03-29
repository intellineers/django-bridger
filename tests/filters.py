from django.db.models import Q

from bridger.filters import BooleanFilter, CharFilter, DateFilter, DateRangeFilter, FilterSet, NumberFilter
from bridger.filters.defaults import (
    current_month_date_end,
    current_month_date_start,
    current_quarter_date_end,
    current_quarter_date_interval,
    current_quarter_date_start,
)
from bridger.tags.filters import TagFilterMixin

from .models import ModelTest, RelatedModelTest


class PandasFilterSet(FilterSet):

    integer_annotated_lte = NumberFilter(label="Integer Annotated", field_name="integer_annotated", lookup_expr="lte")
    integer_annotated_gte = NumberFilter(label="Integer Annotated", field_name="integer_annotated", lookup_expr="gte")

    class Meta:
        model = ModelTest
        fields = {"integer_field": ["lte", "gte"]}


def latest_date_filter(field, request, view):
    qs = view.get_queryset()
    if qs.exists():
        return qs.earliest("date_field").date_field
    return None


class ModelTestFilterSet(TagFilterMixin, FilterSet):

    before_2k = BooleanFilter(label="Before 2k", method="filter_2k")

    datetime_field = DateFilter(
        label="DateTime", lookup_expr="gte", field_name="datetime_field", required=True, default=latest_date_filter,
    )

    # date_field = DateRangeFilter(label="Date", default=current_quarter_date_interval)

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
            # "datetime_field": ["lte", "gte"],
            "status_field": ["exact"],
            "decimal_field": ["lte", "gte", "lt", "gt", "exact"],
            # "before_2k": ["exact", "icontains"],
            "related_models": ["exact"],
        }


class RelatedModelTestFilterSet(TagFilterMixin, FilterSet):
    # char_field = CharFilter(lookup_expr="icontains")

    class Meta:
        model = RelatedModelTest
        # fields = ["char_field", "model_test"]
        fields = {"char_field": ["exact", "icontains"], "model_test": ["exact"]}


class CalendarFilter(FilterSet):

    start = DateFilter(label="Date", lookup_expr="gte", field_name="date_field", method="start_filter",)
    end = DateFilter(label="Date", lookup_expr="lte", field_name="date_field", method="end_filter",)

    def start_filter(self, queryset, name, value):
        return queryset.filter(Q(datetime_field__date__gte=value) & Q(datetime_field1__date__gte=value))

    def end_filter(self, queryset, name, value):
        return queryset.filter(Q(datetime_field__date__lte=value) & Q(datetime_field1__date__lte=value))

    class Meta:
        model = ModelTest
        fields = ["start", "end"]
