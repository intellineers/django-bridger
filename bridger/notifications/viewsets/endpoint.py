from bridger.endpoints.metadata_config import EndpointConfig
from rest_framework.reverse import reverse

class NotificationEndpointConfig(EndpointConfig):
    def get_endpoint(self):
        return None

    def get_create_endpoint(self):
        return None
        
    def get_list_endpoint(self):
        return reverse("bridger:notification-list", request=self.request)

    def get_instance_endpoint(self):
        if self.instance:
            return None
        return self.get_list_endpoint()


