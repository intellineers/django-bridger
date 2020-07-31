from typing import Any, Dict

from rest_framework.metadata import BaseMetadata
from rest_framework.request import Request
from rest_framework.views import View

from .mixins import BridgerViewSetConfig


class BridgerMetadata(BaseMetadata):

    def determine_metadata(self, request: Request, view: View) -> Dict[str, Any]:
        metadata = dict()
        for _class in filter(lambda _klass: "Button" in _klass.__name__, BridgerViewSetConfig.__subclasses__()):
            instance = "pk" in view.kwargs

            try:
                config_class = getattr(view, _class.get_metadata_fieldname())
                config = config_class(view=view, request=request, instance=instance)
            except NotImplementedError:
                config = _class(view=view, request=request, instance=instance)

            sub_metadata = getattr(config, _class.get_metadata_method())()
            try:
                metadata[_class.get_metadata_key()] = dict(sub_metadata)
            except (ValueError, TypeError) as e:
                print(e)
                metadata[_class.get_metadata_key()] = sub_metadata

        return metadata