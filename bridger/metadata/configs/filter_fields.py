from typing import Dict

from bridger.metadata.mixins import BridgerViewSetConfig
from bridger.filters import DjangoFilterBackend
from bridger.utils import ilen

class FilterFieldsBridgerViewSetConfig(BridgerViewSetConfig):

    def get_metadata(self) -> str:
        if DjangoFilterBackend in getattr(self.view, "filter_backends", []):
            filterset_class = DjangoFilterBackend().get_filterset_class(self.view, self.view.queryset)
            if hasattr(filterset_class, "base_filters"):
                filterset = filterset_class.base_filters.items()
                field_names = [v.field_name for k, v in filterset_class.base_filters.items()]
                stored_fields = dict()
                for index, (name, field) in enumerate(filterset):

                    upcomming_fields = ilen(filter(lambda f: f == field.field_name, field_names[index + 1 :]))
                    representation = field.get_representation(self.request, name, self.view)

                    if upcomming_fields > 0 or field.field_name in stored_fields:
                        _representation = stored_fields.get(field.field_name, representation)
                        _representation["lookup_expr"].update(representation["lookup_expr"])
                        _representation["default"].update(representation["default"])
                        stored_fields[field.field_name] = _representation

                    if upcomming_fields == 0:
                        yield field.field_name, stored_fields.get(field.field_name, representation)

    @classmethod
    def get_metadata_key(cls):
        return "filter_fields"
