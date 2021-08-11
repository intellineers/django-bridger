from typing import Dict

from bridger.metadata.mixins import BridgerViewSetConfig
from bridger.filters import DjangoFilterBackend
from bridger.utils import ilen

class FilterFieldsBridgerViewSetConfig(BridgerViewSetConfig):

    def get_metadata(self) -> str:
        for backend in getattr(self.view, "filter_backends", []):
            if isinstance(backend(), DjangoFilterBackend):
                filterset_class = backend().get_filterset_class(self.view, self.view.queryset)
                if filterset_class:
                    base_filters = getattr(filterset_class, "base_filters", {})
                    if filterset_class_meta := getattr(filterset_class, "Meta", None):
                        base_filters.update(getattr(filterset_class_meta, "df_fields", {}))
                    if base_filters:
                        field_names = [v.field_name for k, v in base_filters.items()]
                        stored_fields = dict()
                        for index, (name, field) in enumerate(base_filters.items()):

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
