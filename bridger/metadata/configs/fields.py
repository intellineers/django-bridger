from typing import Dict

from bridger.metadata.mixins import BridgerViewSetConfig
from bridger.serializers import ListSerializer, RepresentationSerializer, percent_decorator

class FieldsBridgerViewSetConfig(BridgerViewSetConfig):

    def get_metadata(self) -> str:
        if not hasattr(self.view, "get_serializer"):
            return None
            
        if serializer := self.view.get_serializer():
            fields = dict()
            rs = RepresentationSerializer
            ls = ListSerializer
            field_items = serializer.fields.items()

            for name, field in filter(lambda f: not isinstance(f[1], (rs, ls)), field_items):
                fields[name] = field.get_representation(self.request, name)

            for name, field in filter(lambda f: isinstance(f[1], (rs, ls)), field_items):
                representation = field.get_representation(self.request, name)
                fields[representation["related_key"]].update(representation)
                del fields[representation["related_key"]]["related_key"]

            serializer_class = self.view.get_serializer_class()

            for key, value in serializer_class.get_decorators():
                fields[key]["decorators"].append(value)
            for key in serializer_class.get_percent_fields():
                fields[key]["type"] = "percent"
                fields[key]["decorators"].append(percent_decorator)

            return fields

    @classmethod
    def get_metadata_key(cls):
        return "fields"
