import logging
import uuid

import django_filters
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .filters import BooleanFilter, CharFilter, ModelChoiceFilter
from .serializers import ModelSerializer, PrimaryKeyCharField
from .settings import bridger_settings
from .viewsets import InfiniteDataModelView

logger = logging.getLogger(__name__)


class FrontendUserConfiguration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(to=get_user_model(), related_name="configurations", on_delete=models.CASCADE)

    parent_configuration = models.ForeignKey(
        to="self", related_name="child_configurations", null=True, blank=True, on_delete=models.CASCADE,
    )
    config = JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return f"{self.user} {self.id}"

    class Meta:
        verbose_name = "Frontend User Settings"
        verbose_name_plural = "Frontend User Settings"


class FrontendUserConfigurationModelSerializer(ModelSerializer):
    id = PrimaryKeyCharField()

    def validate(self, data):
        data["user"] = self.context["request"].user
        return super().validate(data)

    class Meta:
        model = FrontendUserConfiguration
        fields = ["id", "parent_configuration", "config"]


class FrontendUserConfigurationFilterSet(django_filters.rest_framework.FilterSet):
    is_root = BooleanFilter(label="Is Root", method="get_is_root")
    parent_configuration = ModelChoiceFilter(label="Parent Configuration", queryset=FrontendUserConfiguration.objects.all())
    config = CharFilter(label="Config", method="filter_config")

    def get_is_root(self, queryset, name, value):
        return queryset.filter(parent_configuration__isnull=value)

    def filter_config(self, queryset, name, value):
        try:
            key, value = value.split(":")
            if value in ["true", "false"]:
                value = True if value == "true" else False
            return queryset.filter(**{f"config__{key}": value})
        except ValueError:
            return queryset

    class Meta:
        model = FrontendUserConfiguration
        fields = ["is_root", "config"]


class FrontendUserConfigurationModelViewSet(InfiniteDataModelView):
    INSTANCE_BUTTONS = LIST_BUTTONS = []
    serializer_class = FrontendUserConfigurationModelSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filter_class = FrontendUserConfigurationFilterSet

    ordering_fields = ordering = [
        "id",
        *bridger_settings.DEFAULT_FRONTEND_USER_CONFIGURATION_ORDER,
    ]

    def get_queryset(self):
        return FrontendUserConfiguration.objects.filter(user=self.request.user)
