from datetime import date, datetime
from enum import Enum, auto

import django_filters
from django.utils.timezone import localdate
from django.utils.dateparse import parse_date
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.reverse import reverse

from bridger.filters.mixins import BridgerFilterMixin

# from wbutils.dates import get_end_date_from_date, get_start_and_from_date


class ChoiceFilter(BridgerFilterMixin, django_filters.ChoiceFilter):

    filter_type = "select"

    def __init__(self, *args, **kwargs):
        self.choices = kwargs["choices"]
        super().__init__(*args, **kwargs)

    def get_representation(self, request, name, view):
        representation = super().get_representation(request, name, view)
        representation["choices"] = list()
        for choice in self.choices:
            representation["choices"].append({"value": choice[0], "label": choice[1]})
        return representation


class MultipleChoiceFilter(BridgerFilterMixin, django_filters.MultipleChoiceFilter):

    filter_type = "select"

    def __init__(self, *args, **kwargs):
        self.choices = kwargs["choices"]
        # self.widget = django_filters.widgets.QueryArrayWidget
        super().__init__(*args, **kwargs)

    def get_representation(self, request, name, view):
        representation = super().get_representation(request, name, view)
        representation["multiple"] = True
        representation["choices"] = list()
        for choice in self.choices:
            representation["choices"].append({"value": choice[0], "label": choice[1]})
        return representation


class ModelMultipleChoiceFilter(
    BridgerFilterMixin, django_filters.ModelMultipleChoiceFilter
):

    filter_type = "select"

    def __init__(self, *args, **kwargs):
        self.endpoint = kwargs.pop("endpoint", None)
        self.value_key = kwargs.pop("value_key", None)
        self.label_key = kwargs.pop("label_key", None)

        # TODO: This is monkeypatched. Make sure that the CSVWidget is set here and only here!
        if "widget" not in kwargs:
            kwargs["widget"] = django_filters.widgets.CSVWidget
        super().__init__(*args, **kwargs)

    def get_representation(self, request, name, view):
        representation = super().get_representation(request, name, view)
        representation["multiple"] = True

        if hasattr(self.queryset.model, "get_label_key"):
            label_key = self.queryset.model.get_label_key()
        else:
            label_key = self.label_key

        representation["endpoint"] = {
            "url": reverse(self.endpoint, request=request),
            "value_key": self.value_key,
            "label_key": label_key,
        }
        return representation


class ModelChoiceFilter(BridgerFilterMixin, django_filters.ModelChoiceFilter):

    filter_type = "select"

    def __init__(self, *args, **kwargs):
        self.endpoint = kwargs.pop("endpoint", None)
        self.value_key = kwargs.pop("value_key", None)
        self.label_key = kwargs.pop("label_key", None)
        super().__init__(*args, **kwargs)

    def get_representation(self, request, name, view):
        representation = super().get_representation(request, name, view)
        representation["endpoint"] = {
            "url": reverse(self.endpoint, request=request),
            "value_key": self.value_key,
            "label_key": self.label_key,
        }
        return representation


class TimeFilter(BridgerFilterMixin, django_filters.TimeFilter):
    filter_type = "time"


class DateTimeFilter(BridgerFilterMixin, django_filters.DateFilter):
    filter_type = "datetime"


class DateFilter(BridgerFilterMixin, django_filters.DateFilter):
    filter_type = "date"


class DateRangeFilter(BridgerFilterMixin, django_filters.CharFilter):
    filter_type = "daterange"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_representation(self, request, name, view):
        self.key = name
        representation = {
            "label": self.label,
            "type": self.filter_type,
            "key": self.field_name,
        }

        if self.default:
            if callable(self.default):
                default = self.default(field=self, request=request, view=view)
            else:
                default = self.default

            representation["default"] = f"{default[0] or ''},{default[1] or ''}"

        return representation

    def filter(self, qs, value):
        start, end = [parse_date(date_string) for date_string in value.split(",")]

        if start:
            qs = qs.filter(**{f"{self.field_name}__gte": start})

        if end:
            qs = qs.filter(**{f"{self.field_name}__lte": end})

        return qs


class CharFilter(BridgerFilterMixin, django_filters.CharFilter):
    filter_type = "text"


class BooleanFilter(BridgerFilterMixin, django_filters.BooleanFilter):
    filter_type = "boolean"


class NumberFilter(BridgerFilterMixin, django_filters.NumberFilter):
    filter_type = "number"

    def __init__(self, precision=0, *args, **kwargs):
        self.precision = precision
        super().__init__(*args, **kwargs)

    def get_representation(self, request, name, view):
        representation = super().get_representation(request, name, view)
        representation["precision"] = self.precision
        return representation
