from django.db import models
from django.db.models.fields.related import (ManyToManyRel, ManyToOneRel,
                                             OneToOneRel)
from django_filters.filterset import remote_queryset
from django_filters.rest_framework import FilterSet as DjangoFilterSet

from bridger.filters import fields


class FilterSet(DjangoFilterSet):
    FILTER_DEFAULTS = {
        models.BooleanField: {"filter_class": fields.BooleanFilter},
        models.NullBooleanField: {"filter_class": fields.BooleanFilter},
        models.CharField: {"filter_class": fields.CharFilter},
        models.TextField: {"filter_class": fields.CharFilter},
        models.SlugField: {"filter_class": fields.CharFilter},
        models.EmailField: {"filter_class": fields.CharFilter},
        models.FilePathField: {"filter_class": fields.CharFilter},
        models.URLField: {"filter_class": fields.CharFilter},
        models.GenericIPAddressField: {"filter_class": fields.CharFilter},
        models.CommaSeparatedIntegerField: {"filter_class": fields.CharFilter},
        models.DateField: {"filter_class": fields.DateFilter},
        # models.AutoField: {"filter_class": NumberFilter},
        # models.DateTimeField: {"filter_class": DateTimeFilter},
        # models.TimeField: {"filter_class": TimeFilter},
        # models.DurationField: {"filter_class": DurationFilter},
        # models.DecimalField: {"filter_class": NumberFilter},
        # models.SmallIntegerField: {"filter_class": NumberFilter},
        # models.IntegerField: {"filter_class": NumberFilter},
        # models.PositiveIntegerField: {"filter_class": NumberFilter},
        # models.PositiveSmallIntegerField: {"filter_class": NumberFilter},
        # models.FloatField: {"filter_class": NumberFilter},
        # models.UUIDField: {"filter_class": UUIDFilter},
        # Forward relationships
        models.OneToOneField: {
            "filter_class": fields.ModelChoiceFilter,
            "extra": lambda f: {
                "queryset": remote_queryset(f),
                "to_field_name": f.remote_field.field_name,
                "null_label": settings.NULL_CHOICE_LABEL if f.null else None,
            },
        },
        models.ForeignKey: {
            "filter_class": fields.ModelChoiceFilter,
            "extra": lambda f: {
                "queryset": remote_queryset(f),
                "to_field_name": f.remote_field.field_name,
                "null_label": settings.NULL_CHOICE_LABEL if f.null else None,
            },
        },
        models.ManyToManyField: {
            "filter_class": fields.ModelMultipleChoiceFilter,
            "extra": lambda f: {"queryset": remote_queryset(f)},
        },
        # Reverse relationships
        OneToOneRel: {
            "filter_class": fields.ModelChoiceFilter,
            "extra": lambda f: {
                "queryset": remote_queryset(f),
                "null_label": settings.NULL_CHOICE_LABEL if f.null else None,
            },
        },
        ManyToOneRel: {
            "filter_class": fields.ModelMultipleChoiceFilter,
            "extra": lambda f: {"queryset": remote_queryset(f)},
        },
        ManyToManyRel: {
            "filter_class": fields.ModelMultipleChoiceFilter,
            "extra": lambda f: {"queryset": remote_queryset(f)},
        },
    }

    @classmethod
    def filter_for_lookup(cls, field, lookup_type):

        filter_class, params = super().filter_for_lookup(field, lookup_type)
        if hasattr(field, "verbose_name"):
            params["label"] = field.verbose_name

        return filter_class, params
