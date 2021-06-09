
from bridger.endpoints.metadata_config import EndpointConfig
from rest_framework.reverse import reverse

class ClubHouseEndpointConfig(EndpointConfig):
    def get_list_endpoint(self, **kwargs):
        return reverse(f"bridger:clubhouse-list", request=self.request)

    def get_instance_endpoint(self, **kwargs):
        return self.get_list_endpoint()

    def get_create_endpoint(self, **kwargs):
        return self.get_list_endpoint()