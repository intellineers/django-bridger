from typing import Tuple

from rest_framework.request import Request
from rest_framework.views import View

class BridgerViewSetConfig:

    def __init__(self, view: View, request: Request, instance: bool):
        self.view = view
        self.request = request
        self.instance = instance

    @classmethod
    def get_metadata_parameters(cls) -> Tuple[str, str]:
        """ Returns the parameters needed to get the metadata from a config

        Parameters: Fieldname, Methodname
        """
        raise NotImplementedError("This needs to be implemented.")

    @classmethod
    def get_metadata_key(cls):
        raise NotImplementedError()

    @classmethod
    def get_metadata_fieldname(cls):
        raise NotImplementedError()

    @classmethod
    def get_metadata_method(cls):
        return "get_metadata"
