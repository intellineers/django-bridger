import pandas as pd
from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from bridger.metadata.views import MetadataMixin

from .metadata import PandasMetadata


class PandasAPIView(MetadataMixin, APIView):

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
        assert hasattr(
            self, "queryset"
        ), "Either specify a queryset or implement the get_queryset method."
        return self.queryset

    def get_dataframe(self, request):
        assert hasattr(self, "pandas_fields"), "No pandas_fields specified"
        queryset = self.filter_queryset(self.get_queryset())
        return pd.DataFrame(queryset.values(*self.pandas_fields.to_dict().keys()))

    def manipulate_dataframe(self, df):
        return df

    def get_aggregates(self, request, df):
        return {}

    def get(self, request):
        df = self.manipulate_dataframe(self.get_dataframe(request))
        aggregates = self.get_aggregates(request, df)
        return Response({"results": df.T.to_dict().values(), "aggregates": aggregates})
