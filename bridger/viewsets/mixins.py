from contextlib import suppress

from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import CreateModelMixin as OriginalCreateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.mixins import ListModelMixin as OriginalListModelMixin
from rest_framework.mixins import RetrieveModelMixin as OriginalRetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin as OriginalUpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response

from bridger.filters import DjangoFilterBackend
from bridger.messages import serialize_messages


class FilterMixin:
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    filter_fields = {}
    search_fields = []
    ordering_fields = ordering = ("id",)


class ModelMixin:
    @classmethod
    def get_model(cls):
        try:
            if hasattr(cls, "queryset"):
                return cls.queryset.model
            elif hasattr(cls, "serializer_class"):
                return cls.serializer_class.Meta.model
            else:
                return None
        except AttributeError:
            return None


class ListModelMixin(OriginalListModelMixin):
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            with suppress(TypeError, AttributeError):
                messages = self.get_messages(
                    request=request, queryset=queryset, paginated_queryset=page, initial=self._paginator.is_initial(),
                )
                response.data["messages"] = serialize_messages(messages)

            with suppress(TypeError, AttributeError):
                response.data["aggregates"] = self.get_aggregates(queryset=queryset, paginated_queryset=page)
        else:
            serializer = self.get_serializer(queryset, many=True)
            response = Response(serializer.data)
            response.data = {"results": response.data}
            with suppress(TypeError, AttributeError):
                messages = self.get_messages(request=request, queryset=queryset, initial=True)
                response.data["messages"] = serialize_messages(messages)

            with suppress(TypeError, AttributeError):
                response.data["aggregates"] = self.get_aggregates(queryset=queryset)

        return response


class RetrieveModelMixin(OriginalRetrieveModelMixin):
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data = {"instance": response.data}

        with suppress(AttributeError, TypeError):
            messages = self.get_messages(request=request, instance=self.get_object())
            response.data["messages"] = [dict(message) for message in messages]

        return response


class CreateModelMixin(OriginalCreateModelMixin):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {"instance": response.data}
        return response


class UpdateModelMixin(OriginalUpdateModelMixin):
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {"instance": response.data}
        return response


class DestroyMultipleModelMixin:
    def destroy_multiple(self, request, *args, **kwargs):
        model = self.get_serializer_class().Meta.model
        app_label = model._meta.app_label

        queryset = model.objects.filter(id__in=request.data)
        destroyed = self.perform_destroy_multiple(queryset)

        return Response({"count": destroyed[1].get(f"{app_label}.{model.__name__}", 0)}, status=status.HTTP_204_NO_CONTENT,)

    def perform_destroy_multiple(self, queryset):
        return queryset.delete()
