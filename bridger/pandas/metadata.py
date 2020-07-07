from rest_framework.metadata import BaseMetadata

from bridger.enums import WidgetType
from bridger.metadata.fields import (
    ButtonMetadata,
    CreateButtonMetadata,
    CustomButtonMetadata,
    CustomInstanceButtonMetadata,
    EndpointMetadata,
    FieldsMetadata,
    FilterFieldsMetadata,
    IdentifierMetadata,
    InstanceDisplayMetadata,
    ListDisplayMetadata,
    OrderingFieldsMetadata,
    PaginationMetadata,
    PKMetadata,
    SearchFieldsMetadata,
    TitleMetadata,
    WidgetTypeMetadata,
)

# class PandasMetadata(BaseMetadata):
#     def determine_metadata(self, request, view):
#         metadata = defaultdict(dict)

#         metadata["identifier"] = "pandas:1234"
#         metadata["fields"] = view.pandas_fields.to_dict()
#         metadata["list_display"] = view.get_list_display(request)
#         metadata["buttons"] = ["refresh"]

#         # metadata["search_fields"] = view._get_search_fields(request)
#         # metadata["ordering_fields"] = view._get_ordering_fields(request)
#         # metadata["filter_fields"] = {k: v for k, v in view._get_filter_fields(request)}

#         metadata["create_buttons"] = []
#         metadata["custom_buttons"] = []
#         metadata["custom_instance_buttons"] = []

#         # metadata["endpoints"] = view.get_endpoints(
#         #     request=request, buttons=metadata["buttons"]
#         # )
#         # metadata["titles"] = view.get_titles(request=request)
#         return metadata


class PandasMetadata(BaseMetadata):
    def __init__(self, *args, **kwargs):
        self.modules = [
            # IdentifierMetadata,
            # WidgetTypeMetadata,
            TitleMetadata,
            EndpointMetadata,
            ButtonMetadata,
            # CreateButtonMetadata,
            CustomButtonMetadata,
            CustomInstanceButtonMetadata,
            SearchFieldsMetadata,
            OrderingFieldsMetadata,
            FilterFieldsMetadata,
            ListDisplayMetadata,
        ]
        super().__init__(*args, **kwargs)

    def generate_metadata(self, request, view):
        for module in self.modules:
            yield from module(view, request)

    def generate_model_metadata(self, request, view):
        for module in self.model_modules:
            yield from module(view, request)

    def determine_metadata(self, request, view):
        metadata = dict(self.generate_metadata(request, view))

        metadata["type"] = "list"
        metadata["pagination"] = None
        metadata["identifier"] = "pandas:1234"
        metadata["fields"] = view.pandas_fields.to_dict()
        # metadata["buttons"] = ["refresh"]

        return metadata
