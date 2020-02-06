from django.db.models import Q

from bridger.filters import (
    BooleanFilter,
    CharFilter,
    DateFilter,
    DefaultDateRangeFilterValues,
    FilterSet,
)

from .models import ModelTest, RelatedModelTest


class PandasFilterSet(FilterSet):
    char_field = CharFilter(label="Char")

    class Meta:
        model = ModelTest
        fields = ["char_field"]


class ModelTestFilterSet(FilterSet):
    pass

    # # char_field = CharFilter(label="Char")
    # before_2k = BooleanFilter(label="Before 2k", method="filter_2k")
    # date_lte = DateFilter(label="Date", lookup_expr="lte", field_name="date_field",)
    # date_gte = DateFilter(label="Date", lookup_expr="gte", field_name="date_field",)

    # def filter_2k(self, queryset, name, value):
    #     if value:
    #         return queryset.filter(date_field__year__lt=2000)
    #     return queryset

    # class Meta:
    #     model = ModelTest
    #     fields = ["char_field", "date_lte", "date_gte", "before_2k"]
    #     fields = {
    #         "integer_field": ["lte", "gte", "exact"],
    #         "char_field": ["exact", "icontains"],
    #     }


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
