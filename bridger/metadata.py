from django.contrib.contenttypes.models import ContentType
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters
from rest_framework.metadata import SimpleMetadata
from rest_framework.pagination import CursorPagination, LimitOffsetPagination
from rest_framework.reverse import reverse

# from wbutils import serializers as wb_serializers
# from wbutils.filters import DynamicDjangoFilterBackend


class BridgerMetaData(SimpleMetadata):

    pagination = {
        CursorPagination.__name__: "cursor",
        "AggregateCursorPagination": "cursor",
        LimitOffsetPagination.__name__: "page",
        "DataCursorPagination": "cursor",
    }

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
        metadata = dict()

        metadata["identifier"] = view.get_identifier(request)

        metadata["messages"] = view.get_messages(request)

        chart_display = view.get_chart_display()
        if chart_display:
            metadata["type"] = "chart"

        if hasattr(view, "get_serializer"):
            calendar_display = view.get_calendar_display()
            if calendar_display:
                metadata["type"] = "calendar"
            elif "pk" in view.kwargs:
                metadata["type"] = "instance"
                metadata["pk"] = view.kwargs["pk"]
            else:
                metadata["type"] = "list"

            metadata["list_endpoint"] = view.get_list_endpoint(request)
            metadata["instance_endpoint"] = view.get_instance_endpoint(request)
            metadata["new_instance_endpoint"] = view.get_new_instance_endpoint(request)
            metadata["instance_display"] = view.get_instance_display(request)
            metadata["list_display"] = view.get_list_display(request)
            metadata["list_formatting"] = view.get_list_formatting(request)
            metadata["cell_formatting"] = view.get_cell_formatting(request)
            metadata["legends"] = view.get_legends(request)

            metadata["instance_buttons"] = view.get_instance_buttons(request)
            metadata["list_buttons"] = view.get_list_buttons(request)

            metadata["custom_list_buttons"] = view.get_custom_list_buttons(request)
            metadata["custom_instance_buttons"] = view.get_custom_instance_buttons(
                request
            )
            metadata[
                "custom_list_instance_buttons"
            ] = view.get_custom_list_instance_buttons(request)

            metadata["list_widget_title"] = view.get_list_widget_title()
            metadata["instance_widget_title"] = view.get_instance_widget_title()
            metadata["new_instance_widget_title"] = view.get_new_instance_widget_title()

            if view.pagination_class:
                metadata["pagination_type"] = self.pagination[
                    view.pagination_class.__name__
                ]

            metadata["fields"] = dict()

            related_fields = dict()
            for field_name, field in view.get_serializer().fields.items():
                representation = self.get_field_representation(
                    request, field_name, field
                )
                if "related_key" in representation:
                    related_fields[representation["related_key"]] = representation
                else:
                    metadata["fields"][field_name] = representation

            self.check_for_metadata_in_serializer(request, view, metadata)

            for key, value in related_fields.items():
                metadata["fields"][key].update(value)
                del metadata["fields"][key]["related_key"]

        for backend in view.filter_backends:
            backend_obj = backend()
            if type(backend_obj) == filters.SearchFilter:
                metadata["search_fields"] = list(view.search_fields)

            if not chart_display:
                if type(backend_obj) == filters.OrderingFilter:
                    metadata["ordering_fields"] = list(view.ordering_fields)

            if type(backend_obj) in [DjangoFilterBackend]:
                # if type(backend_obj) in [DjangoFilterBackend, DynamicDjangoFilterBackend]:
                metadata["filter_fields"] = dict()

                if type(backend_obj) is DynamicDjangoFilterBackend:
                    filterset = backend_obj.get_filterset_class_from_view(view)
                else:
                    filterset = backend_obj.get_filterset_class(view)

                related_filter = dict()

                for name, f in filterset.base_filters.items():
                    representation = self.get_filter_representation(f, request, name)
                    if "combined_key" in representation:
                        related_filter[name] = representation
                    else:
                        metadata["filter_fields"][name] = representation

                for key, value in related_filter.items():
                    if value["combined_key"] not in metadata["filter_fields"]:
                        metadata["filter_fields"][value["combined_key"]] = dict()

                    for k, v in value.items():
                        if type(v) is dict:
                            if (
                                k
                                not in metadata["filter_fields"][value["combined_key"]]
                            ):
                                metadata["filter_fields"][value["combined_key"]][
                                    k
                                ] = dict()

                            for _k, _v in v.items():
                                metadata["filter_fields"][value["combined_key"]][k][
                                    _k
                                ] = _v
                        else:
                            metadata["filter_fields"][value["combined_key"]][k] = v
                    metadata["filter_fields"][value["combined_key"]]["key"] = value[
                        "combined_key"
                    ]
                    del metadata["filter_fields"][value["combined_key"]]["combined_key"]

        return metadata
