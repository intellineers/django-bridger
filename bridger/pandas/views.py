from rest_framework.response import Response
from rest_framework.views import APIView
from .metadata import PandasMetadata
from bridger.mixins import MetadataMixin
import pandas as pd


class PandasAPIView(MetadataMixin, APIView):

    metadata_class = PandasMetadata

    def get_queryset(self, request):
        assert hasattr(
            self, "queryset"
        ), "Either specify a queryset or implement the get_queryset method."
        return self.queryset

    def get_dataframe(self, request):
        assert hasattr(self, "pandas_fields"), "No pandas_fields specified"
        return pd.DataFrame(
            self.get_queryset(request).values(*self.pandas_fields.to_dict().keys())
        )

    def get_aggregates(self, request, df):
        return df

    def get(self, request):
        df = self.get_dataframe(request)
        aggregates = self.get_aggregates(request, df)
        return Response({"results": df.T.to_dict().values(), "aggregates": aggregates})
