import pandas as pd
from django.db.models import QuerySet
from rest_framework import filters
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from bridger.filters import DjangoFilterBackend
from bridger.metadata.views import MetadataMixin
from bridger.viewsets.mixins import DocumentationMixin, ModelMixin
from .metadata import PandasMetadata


class PandasAPIView(MetadataMixin, DocumentationMixin, ModelMixin, APIView):

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]

    metadata_class = PandasMetadata

    filter_fields = {}
    search_fields = []
    ordering_fields = []

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get_queryset(self):
        assert hasattr(self, "queryset"), "Either specify a queryset or implement the get_queryset method."
        return self.queryset

    def get_dataframe(self, request):
        assert hasattr(self, "pandas_fields"), "No pandas_fields specified"
        queryset = self.filter_queryset(self.get_queryset())
        if queryset.exists():
            return pd.DataFrame(queryset.values(*self.pandas_fields.to_dict().keys()))
        return pd.DataFrame()

    def manipulate_dataframe(self, df):
        return df

    def get_aggregates(self, request, df):
        return {}

    def get(self, request):
        self.request = request
        df = self.manipulate_dataframe(self.get_dataframe(request))
        df.where(pd.notnull(df), None)
        aggregates = self.get_aggregates(request, df) if not df.empty else {}
        return Response({"results": df.T.to_dict().values(), "aggregates": aggregates})
