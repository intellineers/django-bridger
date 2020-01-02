from collections import defaultdict

from django.contrib.contenttypes.models import ContentType
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters
from rest_framework.metadata import SimpleMetadata
from rest_framework.pagination import CursorPagination, LimitOffsetPagination
from rest_framework.reverse import reverse

from .enums import WidgetType

# from wbutils import serializers as wb_serializers
# from wbutils.filters import DynamicDjangoFilterBackend


class BridgerMetaData(SimpleMetadata):
    def get_filter_representation(self, filter_field, request, name):
        if hasattr(filter_field, "get_representation"):
            return filter_field.get_representation(request, name)

        return {"label": filter_field.label}

    def get_field_representation(self, request, field_name, field):
        if hasattr(field, "get_representation"):
            return field.get_representation(request, field_name)

        return {
            "key": field_name,
            "label": field.label,
            "type": self.label_lookup[field],
            "required": getattr(field, "required", False),
            "read_only": getattr(field, "read_only", False),
        }

    def check_for_metadata_in_serializer(self, request, view, metadata):
        serializer = view.get_serializer_class()
        if serializer:
            meta = serializer.Meta

            decorators = getattr(meta, "decorators", dict())
            for key, value in decorators.items():
                metadata["fields"][key]["decorators"] = value

            percent_fields = getattr(meta, "percent_fields", list())
            for percent_field in percent_fields:
                metadata["fields"][percent_field]["type"] = "percent"

    def determine_metadata(self, request, view):
        metadata = defaultdict(dict)

        metadata["type"] = view.get_widget_type(request=request)
        metadata["identifier"] = view.get_identifier(request=request)
        metadata["buttons"] = view.get_buttons(request=request)
        metadata["endpoints"] = view.get_endpoints(
            request=request, buttons=metadata["buttons"]
        )
        metadata["pagination"] = view.get_pagination(request=request)

        if metadata["type"] in [WidgetType.INSTANCE.value, WidgetType.LIST.value]:
            serializer_class = view.get_serializer_class()
            if "pk" in view.kwargs:
                metadata["pk"] = view.kwargs["pk"]

            metadata["list_display"] = view.get_list_display(request)
            metadata["instance_display"] = view.get_instance_display(request)

            metadata["fields"] = view.get_fields(request)
            for key, value in serializer_class.get_decorators():
                metadata["fields"][key]["decorators"] = value
            for key in serializer_class.get_percent_fields():
                metadata["fields"][key]["type"] = "percent"

        # TODO: Messages
        # TODO: Legends
        # TODO: Custom Buttons
        # TODO: Titles
        # TODO: Pagination

        # for backend in view.filter_backends:
        #     backend_obj = backend()
        #     if type(backend_obj) == filters.SearchFilter:
        #         metadata["search_fields"] = list(view.search_fields)

        #     if not chart_display:
        #         if type(backend_obj) == filters.OrderingFilter:
        #             metadata["ordering_fields"] = list(view.ordering_fields)

        #     if type(backend_obj) in [DjangoFilterBackend]:
        #         # if type(backend_obj) in [DjangoFilterBackend, DynamicDjangoFilterBackend]:
        #         metadata["filter_fields"] = dict()

        #         if type(backend_obj) is DynamicDjangoFilterBackend:
        #             filterset = backend_obj.get_filterset_class_from_view(view)
        #         else:
        #             filterset = backend_obj.get_filterset_class(view)

        #         related_filter = dict()

        #         for name, f in filterset.base_filters.items():
        #             representation = self.get_filter_representation(f, request, name)
        #             if "combined_key" in representation:
        #                 related_filter[name] = representation
        #             else:
        #                 metadata["filter_fields"][name] = representation

        #         for key, value in related_filter.items():
        #             if value["combined_key"] not in metadata["filter_fields"]:
        #                 metadata["filter_fields"][value["combined_key"]] = dict()

        #             for k, v in value.items():
        #                 if type(v) is dict:
        #                     if (
        #                         k
        #                         not in metadata["filter_fields"][value["combined_key"]]
        #                     ):
        #                         metadata["filter_fields"][value["combined_key"]][
        #                             k
        #                         ] = dict()

        #                     for _k, _v in v.items():
        #                         metadata["filter_fields"][value["combined_key"]][k][
        #                             _k
        #                         ] = _v
        #                 else:
        #                     metadata["filter_fields"][value["combined_key"]][k] = v
        #             metadata["filter_fields"][value["combined_key"]]["key"] = value[
        #                 "combined_key"
        #             ]
        #             del metadata["filter_fields"][value["combined_key"]]["combined_key"]

        return metadata
