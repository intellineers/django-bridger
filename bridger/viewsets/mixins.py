import inspect
from contextlib import suppress
from pathlib import Path

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from markdown import markdown
from markdown.extensions.tables import TableExtension
from markdown_blockdiag import BlockdiagExtension
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import CreateModelMixin as OriginalCreateModelMixin
from rest_framework.mixins import DestroyModelMixin as OriginalDestroyModelMixin
from rest_framework.mixins import ListModelMixin as OriginalListModelMixin
from rest_framework.mixins import RetrieveModelMixin as OriginalRetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin as OriginalUpdateModelMixin
from rest_framework.renderers import StaticHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED, HTTP_204_NO_CONTENT
from slugify import slugify

from bridger.auth import JWTCookieAuthentication
from bridger.filters import DjangoFilterBackend
from bridger.fsm.markdown_extensions import FSMExtension
from bridger.messages import serialize_messages


class FilterMixin:
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    filter_fields = {}
    search_fields = []
    ordering_fields = ordering = ("id",)


class DocumentationMixin:

    def _get_documentation_path(self, detail):
        default_path = Path(inspect.getfile(self.__class__)).parent / "documentation" / f"{slugify(self.__class__.__name__)}.md"
        custom_path = getattr(self, "INSTANCE_DOCUMENTATION", None) if detail else getattr(self, "LIST_DOCUMENTATION", None)

        if custom_path and Path(custom_path).exists():
            return Path(custom_path)

        if default_path.exists():
            return default_path

        return None

    def _render_documentation(self, path, detail):
        with open(path, "r") as f:
            content = markdown(f.read(), extensions=[TableExtension(), FSMExtension(), BlockdiagExtension(format="svg")])
            return content

    @action(
        methods=["get"],
        detail=True,
        authentication_classes=[SessionAuthentication, JWTCookieAuthentication],
        permission_classes=[],
        renderer_classes=[StaticHTMLRenderer],
    )
    def instance_documentation(self, *args, **kwargs):
        if path := self._get_documentation_path(True):
            return HttpResponse(self._render_documentation(path, True))
        return HttpResponse(status=HTTP_404_NOT_FOUND)

    @action(
        methods=["get"],
        detail=False,
        authentication_classes=[SessionAuthentication, JWTCookieAuthentication],
        permission_classes=[],
        renderer_classes=[StaticHTMLRenderer],
    )
    def list_documentation(self, *args, **kwargs):
        if path := self._get_documentation_path(False):
            return HttpResponse(self._render_documentation(path, False))
        return HttpResponse(status=HTTP_404_NOT_FOUND)

class ModelMixin:
    @classmethod
    def get_model(cls):
        try:
            if hasattr(cls, "queryset") and cls.queryset is not None:
                return cls.queryset.model
            elif hasattr(cls, "serializer_class"):
                return cls.serializer_class.Meta.model
            else:
                return None
        except AttributeError:
            return None

    @classmethod
    def get_content_type(cls):
        return ContentType.objects.get_for_model(cls.get_model())


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
        # If not create endpoint is defined then raise 405
        if self.endpoint_config_class(view=self, request=self.request, instance=False)._get_create_endpoint() is None:
            return Response(status=HTTP_405_METHOD_NOT_ALLOWED)

        response = super().create(request, *args, **kwargs)
        response.data = {"instance": response.data}
        return response


class UpdateModelMixin(OriginalUpdateModelMixin):
    def update(self, request, *args, **kwargs):
        # If no instance endpoint is defined, then raise 405
        if self.endpoint_config_class(view=self, request=self.request, instance=True)._get_instance_endpoint() is None:
            return Response(status=HTTP_405_METHOD_NOT_ALLOWED)

        response = super().update(request, *args, **kwargs)
        response.data = {"instance": response.data}
        return response


class DestroyModelMixin(OriginalDestroyModelMixin):
    
    def destroy(self, request, *args, **kwargs):
        # If no delete endpoint is defined, then raise 405
        if self.endpoint_config_class(view=self, request=self.request, instance=True)._get_delete_endpoint() is None:
            return Response(status=HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)


class DestroyMultipleModelMixin:
    def destroy_multiple(self, request, *args, **kwargs):
        # If no delete endpoint is defined, then raise 405
        if self.endpoint_config_class(view=self, request=self.request, instance=False)._get_delete_endpoint() is None:
            return Response(status=HTTP_405_METHOD_NOT_ALLOWED)

        model = self.get_serializer_class().Meta.model
        app_label = model._meta.app_label

        queryset = model.objects.filter(id__in=request.data)
        destroyed = self.perform_destroy_multiple(queryset)
        return Response({"count": destroyed[1].get(f"{app_label}.{model.__name__}", 0)}, status=HTTP_204_NO_CONTENT)

    def perform_destroy_multiple(self, queryset):
        return queryset.delete()
