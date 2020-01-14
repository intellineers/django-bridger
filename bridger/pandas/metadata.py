from collections import defaultdict

from rest_framework.metadata import SimpleMetadata
from rest_framework.reverse import reverse


class PandasMetadata(SimpleMetadata):
    def determine_metadata(self, request, view):
        metadata = defaultdict(dict)
        metadata["type"] = "list"
        metadata["pagination"] = None
        metadata["identifier"] = "pandas:1234"
        metadata["fields"] = view.pandas_fields.to_dict()
        metadata["list_display"] = view.get_list_display(request)
        metadata["buttons"] = ["refresh"]

        metadata["search_fields"] = view.get_search_fields(request)
        metadata["ordering_fields"] = view.get_ordering_fields(request)
        metadata["filter_fields"] = {k: v for k, v in view.get_filter_fields(request)}

        metadata["create_buttons"] = []
        metadata["custom_buttons"] = []
        metadata["custom_instance_buttons"] = []

        metadata["endpoints"] = view.get_endpoints(
            request=request, buttons=metadata["buttons"]
        )
        metadata["titles"] = view.get_titles(request=request)
        return metadata
