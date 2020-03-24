from typing import Dict, Iterator, List, Tuple, Union

from rest_framework.request import Request
from rest_framework.reverse import reverse

from bridger.metadata.mixins import BridgerMetadataMixin

Endpoint_T = Union[str, Tuple[str, List, Dict]]


class EndpointMetadata(BridgerMetadataMixin):
    key = "endpoints"
    method_name = "_get_endpoints"


class EndpointMetadataMixin:
    def get_generic_endpoint(
        self, request: Request, endpoint: Endpoint_T = None
    ) -> Endpoint_T:
        return endpoint

    def _get_generic_endpoint(self, request: Request, endpoint_type: str) -> Endpoint_T:
        field_name = endpoint_type.upper()
        method_name = f"get_{endpoint_type}"

        endpoint = getattr(self, method_name, self.get_generic_endpoint)(
            request, getattr(self, field_name, None)
        )

        if endpoint is None:
            return endpoint

        if isinstance(endpoint, str):
            viewname, args, kwargs = endpoint, [], {}
        else:
            viewname, args, kwargs = endpoint

        return reverse(viewname=viewname, request=request, args=args, kwargs=kwargs)

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

    def _get_endpoints(self, request: Request) -> Iterator[Dict[str, str]]:
        endpoints = dict()

        endpoint = self._get_endpoint(request=request)
        list_endpoint = self._get_list_endpoint(request=request)
        instance_endpoint = self._get_instance_endpoint(request=request)
        create_endpoint = self._get_create_endpoint(request=request)
        delete_endpoint = self._get_delete_endpoint(request=request)

        if list_endpoint or endpoint:
            endpoints["list"] = list_endpoint or endpoint

        if instance_endpoint or endpoint:
            endpoints["instance"] = instance_endpoint or endpoint

        if create_endpoint or endpoint:
            endpoints["create"] = create_endpoint or endpoint

        if delete_endpoint or endpoint:
            endpoints["delete"] = delete_endpoint or endpoint

        return endpoints
