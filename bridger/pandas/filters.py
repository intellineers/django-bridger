"""
Provide Filters for Pandas based views
"""
import operator
from functools import reduce
from bridger import filters as wb_filters
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models.constants import LOOKUP_SEP
from django.template import loader
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from rest_framework.compat import coreapi, coreschema, distinct
from rest_framework.settings import api_settings
from rest_framework.filters import SearchFilter, OrderingFilter
from bridger.filters import DjangoFilterBackend

class PandasDjangoFilterBackend(DjangoFilterBackend):
    lookups_operator = {
        'lte': operator.le,
        'lt': operator.lt,
        'gte': operator.ge,
        'gt': operator.gt,
        'exact': operator.eq
    }
    def filter_dataframe(self, request, df, view):
        filterset_class = self.get_filterset_class(view, view.get_queryset())
        kwargs = self.get_filterset_kwargs(request, view.get_queryset(), view)

        filter_terms = filterset_class(**kwargs).form.data
        pandas_view_fields = view.pandas_fields.to_dict()
        conditions = []
        for filter_term, value in filter_terms.items():
            if _filter := getattr(filterset_class.Meta, "df_fields", {}).get(filter_term, None):
                # We support only number for now
                lookup_expr = getattr(_filter, "lookup_expr", 'exact')
                if isinstance(_filter, wb_filters.NumberFilter):
                    conditions.append(self.lookups_operator[lookup_expr](df[_filter.field_name], float(value)))
        if conditions:
            df = df[reduce(operator.and_, conditions)]
        return df

class PandasSearchFilter(SearchFilter):

    def filter_queryset(self, request, queryset, view):
        return queryset

    def filter_dataframe(self, request, df, view):
        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)
        if not search_fields or not search_terms or df.empty:
            return df

        search_fields = [field for field in search_fields if field in df.columns]
        conditions = []

        for search_term in search_terms:
            queries = [
                df[field].str.contains(search_term, na=False, case=False)
                for field in search_fields
            ]
            conditions.append(reduce(operator.or_, queries))
        df = df[reduce(operator.and_, conditions)]

        return df


class PandasOrderingFilter(OrderingFilter):

    def get_ordering_df(self, request, df, view):
        """
        Ordering is set by a comma delimited ?ordering=... query parameter.

        The `ordering` query parameter can be overridden by setting
        the `ordering_param` value on the OrderingFilter or by
        specifying an `ORDERING_PARAM` value in the API settings.
        """
        params = request.query_params.get(self.ordering_param)
        if params:
            fields = [param.strip() for param in params.split(',')]
            ordering = self.remove_invalid_fields_df(df, fields, view, request)
            if ordering:
                return ordering

        # No ordering was included, or all the ordering fields were invalid
        return self.get_default_ordering(view)

    def remove_invalid_fields_df(self, df, fields, view, request):
        valid_fields = getattr(view, 'ordering_fields', self.ordering_fields)

        def term_valid(term):
            if term.startswith("-"):
                term = term[1:]
            return term in df.columns and term in valid_fields

        return [term for term in fields if term_valid(term)]

    def filter_queryset(self, request, queryset, view):
        return queryset

    def filter_dataframe(self, request, df, view):
        base_ordering = self.get_ordering_df(request, df, view)
        if base_ordering:
            ordering_by = []
            ascending_list = []
            for order in base_ordering:
                ascending = order[0] != '-'
                ordering_by.append(order.replace('-', ''))
                ascending_list.append(ascending)

            if ordering_by and ascending_list:
                return df.sort_values(by=ordering_by, ascending=ascending_list)
        return df