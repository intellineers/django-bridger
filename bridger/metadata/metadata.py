from typing import Any, Dict

from rest_framework.metadata import BaseMetadata
from rest_framework.request import Request
from rest_framework.views import View

from .mixins import BridgerViewSetConfig


class BridgerMetadata(BaseMetadata):

    def determine_metadata(self, request: Request, view: View) -> Dict[str, Any]:
        metadata = dict()

        # Check whether the current view is an instance view
        instance = "pk" in view.kwargs
        
        # Iterate over all subclasses that inherit from BridgerViewSetConfig
        for _class in BridgerViewSetConfig.__subclasses__(): 

            # Try to get the config class in one of two ways:
            # 1. Get it by accessing the instance field behind get_metadata_fieldname (Config classes that should/can be overriden)
            # 2. Use the subclasss (Config classes that should not be overriden)
            try:
                config_class = getattr(view, _class.get_metadata_fieldname())
                config = config_class(view=view, request=request, instance=instance)
            except NotImplementedError:
                config = _class(view=view, request=request, instance=instance)

            # Get the submetadata and if needed. 
            sub_metadata = getattr(config, _class.get_metadata_method())()
            try:
                metadata[_class.get_metadata_key()] = dict(sub_metadata)
            except (ValueError, TypeError) as e:
                metadata[_class.get_metadata_key()] = sub_metadata

        return metadata
