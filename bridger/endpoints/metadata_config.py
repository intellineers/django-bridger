from typing import Tuple, List, Dict, Union

from rest_framework.reverse import reverse
from bridger.metadata.mixins import BridgerViewSetConfig


class EndpointConfig(BridgerViewSetConfig):
    """ Configuration for endpoints to determine which buttons and actions are available

    In Instance Views:
    - instance_endpoint -> Save Button [PATCH|PUT]
    - list_endpoint -> Return to list?
    - delete_endpoint -> Delete Button (Instance) [DELETE]
    - create_endpoint -> Create Button [POST]

    In List Views:
    - instance_endpoint -> Makes instance clickable and opens existing instance [GET] !!With Handlebar for PK
    - list_endpoint -> Means nothing?
    - delete_endpoint -> Delete Button (Batch Delete) [DELETE] !!With Handlebar for PK (not really?)
    - create_endpoint -> Create Buttons [POST]

    """

    PK_FIELD = "id"

    def get_endpoint(self):
        model = self.view.get_model()
        if basename_method := getattr(model, "get_endpoint_basename", None):
            basename = basename_method()
            if self.instance:
                return reverse(f"{basename}-detail", args=[self.view.kwargs.get("pk")], request=self.request)
            else:
                return reverse(f"{basename}-list", request=self.request)
        return None

    def get_instance_endpoint(self):
        return self.get_endpoint()

    def _get_instance_endpoint(self):
        if endpoint := self.get_instance_endpoint():
            content_type = self.view.get_content_type()
            change_permission = f"{content_type.app_label}.change_{content_type.model}"

            read_only = getattr(self.view, "READ_ONLY", False)
            if self.instance and self.request.user.has_perm(change_permission) and not read_only:
                return endpoint 
            elif not self.instance:
                pk_identifier = "{{"+ self.PK_FIELD +"}}/"
                return endpoint + pk_identifier

        return None

    def get_list_endpoint(self):
        return self.get_endpoint()

    def _get_list_endpoint(self):
        return self.get_list_endpoint()

    def get_delete_endpoint(self):
        return self.get_endpoint()

    def _get_delete_endpoint(self):
        read_only = getattr(self.view, "READ_ONLY", False)
        if read_only:
            return None

        if endpoint := self.get_delete_endpoint():
            content_type = self.view.get_content_type()
            delete_permission = f"{content_type.app_label}.delete_{content_type.model}"

            if self.request.user.has_perm(delete_permission):
                return endpoint
        return None

    def get_create_endpoint(self):
        return self.get_endpoint()

    def _get_create_endpoint(self):
        read_only = getattr(self.view, "READ_ONLY", False)
        if read_only:
            return None

        if endpoint := self.get_create_endpoint():
            content_type = self.view.get_content_type()
            create_permission = f"{content_type.app_label}.add_{content_type.model}"

            if self.request.user.has_perm(create_permission):
                return endpoint
        return None
  
    def get_metadata(self) -> Dict:
        yield "instance", self._get_instance_endpoint()
        yield "list", self._get_list_endpoint()
        yield "delete", self._get_delete_endpoint()
        yield "create", self._get_create_endpoint()

    @classmethod
    def get_metadata_key(cls):
        return "endpoints"

    @classmethod
    def get_metadata_fieldname(cls):
        return "endpoint_config_class"

class EndpointConfigMixin:
    endpoint_config_class = EndpointConfig