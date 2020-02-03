from collections import defaultdict

from rest_framework.metadata import SimpleMetadata
from rest_framework.reverse import reverse

from .enums import WidgetType
from .serializers import percent_decorator


class BridgerMetaData(SimpleMetadata):
    def determine_metadata(self, request, view):
        metadata = defaultdict(dict)

        metadata["type"] = view.get_widget_type(request=request)
        metadata["identifier"] = view.get_identifier(request=request)
        metadata["buttons"] = view.get_buttons(request=request)
        metadata["create_buttons"] = view.get_create_buttons(request=request)
        metadata["custom_buttons"] = view.get_custom_buttons(request=request)
        metadata["custom_instance_buttons"] = view.get_custom_instance_buttons(
            request=request
        )
        metadata["preview_buttons"] = view.get_preview_buttons(request=request)
        metadata["preview_display"] = view.get_preview_display(request=request)
        metadata["endpoints"] = view.get_endpoints(
            request=request, buttons=metadata["buttons"]
        )
        metadata["pagination"] = view.get_pagination(request=request)
        metadata["titles"] = view.get_titles(request=request)

        if metadata["type"] in [WidgetType.INSTANCE.value, WidgetType.LIST.value]:
            serializer_class = view.get_serializer_class()
            if "pk" in view.kwargs:
                metadata["pk"] = view.kwargs["pk"]

            metadata["list_display"] = view.get_list_display(request)
            metadata["instance_display"] = view.get_instance_display(request)

            metadata["fields"] = view.get_fields(request)
            for key, value in serializer_class.get_decorators():
                metadata["fields"][key]["decorators"].append(value)
            for key in serializer_class.get_percent_fields():
                metadata["fields"][key]["type"] = "percent"
                metadata["fields"][key]["decorators"].append(percent_decorator)

        metadata["search_fields"] = view.get_search_fields(request)
        metadata["ordering_fields"] = view.get_ordering_fields(request)
        metadata["filter_fields"] = {k: v for k, v in view.get_filter_fields(request)}

        # TODO: Custom Buttons

        return metadata
