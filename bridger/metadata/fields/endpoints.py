from contextlib import suppress
from typing import Dict, Iterator, List, Tuple, Union

from django.urls.exceptions import NoReverseMatch
from rest_framework.request import Request
from rest_framework.reverse import reverse

from bridger.metadata.mixins import BridgerMetadataMixin

Endpoint_T = Union[str, Tuple[str, List, Dict]]


class EndpointMetadata(BridgerMetadataMixin):
    key = "endpoints"
    method_name = "_get_endpoints"


class EndpointMetadataMixin:
    def get_generic_endpoint(self, request: Request, endpoint: Endpoint_T = None) -> Endpoint_T:
        return endpoint

    def get_history_endpoint(self, request, endpoint=None):

        with suppress(AssertionError, AttributeError):
            obj = self.get_object()
            model = type(obj)
            opts = model._meta

            if hasattr(opts, "simple_history_manager_attribute") and hasattr(model, "get_endpoint_basename"):
                return (
                    f"{model.get_endpoint_basename()}-history-list",
                    [obj.id],
                    {},
                )

        return None

    def _get_generic_endpoint(self, request: Request, endpoint_type: str) -> Endpoint_T:
        field_name = endpoint_type.upper()
        method_name = f"get_{endpoint_type}"

        endpoint = getattr(self, method_name, self.get_generic_endpoint)(request, getattr(self, field_name, None))

        if endpoint is None:
            return endpoint

        if isinstance(endpoint, str):
            viewname, args, kwargs = endpoint, [], {}
        else:
            viewname, args, kwargs = endpoint

        try:
            return reverse(viewname=viewname, request=request, args=args, kwargs=kwargs)
        except NoReverseMatch:
            return None

    def get_pk_endpoint_field(self, request: Request) -> str:
        return "{{" + getattr(self, "PK_FIELD", "id") + "}}"

    def _get_endpoint(self, request: Request) -> Endpoint_T:
        return self._get_generic_endpoint(request, "endpoint")

    def _get_list_endpoint(self, request: Request) -> Endpoint_T:
        return self._get_generic_endpoint(request, "list_endpoint")

    def _get_instance_endpoint(self, request: Request) -> Endpoint_T:
        return self._get_generic_endpoint(request, "instance_endpoint")

    def _get_create_endpoint(self, request: Request) -> Endpoint_T:
        return self._get_generic_endpoint(request, "create_endpoint")

    def _get_delete_endpoint(self, request: Request) -> Endpoint_T:
        return self._get_generic_endpoint(request, "delete_endpoint")

    def _get_history_endpoint(self, request: Request) -> Endpoint_T:
        return self._get_generic_endpoint(request, "history_endpoint")

    def _get_endpoints(self, request: Request) -> Iterator[Dict[str, str]]:
        endpoints = dict()

        endpoint = self._get_endpoint(request=request)
        list_endpoint = self._get_list_endpoint(request=request)
        instance_endpoint = self._get_instance_endpoint(request=request)
        create_endpoint = self._get_create_endpoint(request=request)
        delete_endpoint = self._get_delete_endpoint(request=request)
        history_endpoint = self._get_history_endpoint(request=request)

        if not self.kwargs.get("pk", None):
            if url := instance_endpoint or endpoint:
                endpoints["instance"] = f"{url}{self.get_pk_endpoint_field(request)}/"

        else:
            if url := list_endpoint or endpoint:
                endpoints["list"] = url

            if history_endpoint:
                endpoints["history"] = history_endpoint

        if not getattr(self, "READ_ONLY", False):
            if url := create_endpoint or endpoint:
                endpoints["create"] = url

            if url := delete_endpoint or endpoint:
                endpoints["delete"] = f"{url}{self.get_pk_endpoint_field(request)}/"

        return endpoints
