import logging
from typing import Dict, Generator, List, Optional

from django.contrib.contenttypes.models import ContentType
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import CursorPagination, LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.reverse import reverse

from bridger.enums import Button, WidgetType
from bridger.serializers import RepresentationSerializer

from .metadata import BridgerMetaData

logger = logging.getLogger(__name__)


class MetadataMixin:
    """
    A mixin that adds the BridgerMetaData to a View with all functionalities
    needed to properly create a valid OPTION request:

    === IDENTIFIER ===
    The identifier is a unique string which identifies this endpoint. This can be used
    for a frontend caching mechanism.

    === ENDPOINT ===
    The endpoints display the url where something is found. Three different endpoints
    are being supported:
    - instance_endpoint
    - list_endpoint
    - new_instance_endpoint

    === BUTTONS ===
    The buttons describe what kind of buttons are appropriate for this endpoint.

    - buttons: Default buttons which are displayed
       - Options: [save, save_and_new, save_and_close, delete, refresh, new]
    - custom_buttons: Custom Buttons that do stuff
    - custom_instance_buttons: Custom buttons which are tied to additional resources of an instance


    === MESSAGES ===
    Messages that should be conveyed through the OPTIONS request

    === DISPLAY ===
    The displays describe how a list or an instance should be displayed. Essentially,
    they describe a table layout for lists and a form for instances.

    === TITLES ===
    Returns the Widget Titles for Instance, List and Create Widgets

    """

    metadata_class = BridgerMetaData

    def get_widget_type(self, request: Request) -> str:
        widget_type = getattr(self, "WIDGET_TYPE", None)

        return widget_type or (
            WidgetType.LIST.value
            if "pk" not in self.kwargs
            else WidgetType.INSTANCE.value
        )

    def get_identifier(self, request: Request) -> str:
        identifier = getattr(self, "IDENTIFIER", None)
        if not identifier and hasattr(self, "get_serializer_class"):
            ct = ContentType.objects.get_for_model(
                self.get_serializer_class().Meta.model
            )
            return f"{ct.app_label}:{ct.model}"
        assert identifier, "Each Endpoint needs an Identifier"
        return identifier

    def get_endpoint(self, request: Request) -> Optional[str]:
        if hasattr(self, "ENDPOINT"):
            return reverse(self.ENDPOINT, request=request)
        return None

    def get_list_endpoint(self, request: Request) -> Optional[str]:
        if hasattr(self, "LIST_ENDPOINT"):
            return reverse(self.LIST_ENDPOINT, request=request)
        return self.get_endpoint(request=request)

    def get_instance_endpoint(self, request: Request) -> Optional[str]:
        if hasattr(self, "INSTANCE_ENDPOINT"):
            return reverse(self.INSTANCE_ENDPOINT, request=request)
        return self.get_endpoint(request=request)

    def get_create_endpoint(self, request: Request) -> Optional[str]:
        if hasattr(self, "CREATE_ENDPOINT"):
            return reverse(self.CREATE_ENDPOINT, request=request)
        return self.get_endpoint(request=request)

    def get_delete_endpoint(self, request: Request) -> Optional[str]:
        if hasattr(self, "DELETE_ENDPOINT"):
            return reverse(self.DELETE_ENDPOINT, request=request)
        return self.get_endpoint(request=request)

    def get_endpoints(self, request: Request, buttons: List[str]) -> Dict[str, str]:
        endpoints = dict()

        list_endpoint = self.get_list_endpoint(request=request)
        instance_endpoint = self.get_instance_endpoint(request=request)
        create_endpoint = self.get_create_endpoint(request=request)
        delete_endpoint = self.get_instance_endpoint(request=request)

        if list_endpoint:
            endpoints["list"] = list_endpoint

        if instance_endpoint:
            endpoints["instance"] = instance_endpoint

        if create_endpoint:
            endpoints["create"] = create_endpoint
        elif Button.NEW.value in buttons:
            logger.warn(
                "New Button Specified, but no create endpoint specified. New Button is removed."
            )
            buttons.remove(Button.NEW.value)

        if delete_endpoint:
            endpoints["delete"] = delete_endpoint
        elif Button.DELETE.value in buttons:
            logger.warn(
                "Delete Button Specified, but no delete endpoint specified. Delete Button is removed."
            )
            buttons.remove(Button.NEW.value)

        return endpoints

    def get_buttons(self, request: Request) -> List[str]:
        buttons = list()

        pk = self.kwargs.get("pk", None)
        ct = None
        if hasattr(self, "get_serializer_class"):
            ct = ContentType.objects.get_for_model(
                self.get_serializer_class().Meta.model
            )

        if pk:
            if hasattr(self, "INSTANCE_BUTTONS"):
                return self.INSTANCE_BUTTONS
            elif ct:
                if f"{ct.app_label}.change_{ct.model}":
                    buttons.append(Button.SAVE.value)
                if f"{ct.app_label}.delete_{ct.model}":
                    buttons.append(Button.DELETE.value)
        else:
            if hasattr(self, "LIST_BUTTONS"):
                return self.LIST_BUTTONS
            elif ct:
                if f"{ct.app_label}.add_{ct.model}":
                    buttons.append(Button.NEW.value)

        buttons.append(Button.REFRESH.value)
        return buttons

    def get_create_buttons(self, request: Request) -> List[str]:
        return getattr(self, "CREATE_BUTTONS", [])

    def get_custom_buttons(self, request: Request) -> Dict[str, str]:
        return []

    def get_instance_display(self, request: Request) -> List:
        if hasattr(self, "INSTANCE_DISPLAY"):
            return self.INSTANCE_DISPLAY.to_dict()
        return []

    def get_list_display(self, request: Request) -> Dict:
        if hasattr(self, "LIST_DISPLAY"):
            return self.LIST_DISPLAY.to_dict()
        return {}

    def get_fields(self, request: Request) -> Dict:
        fields = dict()
        rs = RepresentationSerializer
        field_items = self.get_serializer().fields.items()

        for name, field in filter(lambda f: not isinstance(f[1], rs), field_items):
            fields[name] = field.get_representation(request, name)

        for name, field in filter(lambda f: isinstance(f[1], rs), field_items):
            representation = field.get_representation(request, name)
            fields[representation["related_key"]].update(representation)
            del fields[representation["related_key"]]["related_key"]

        return fields

    # BUTTONS
    def get_instance_buttons(self, request):
        instance_buttons = getattr(self, "INSTANCE_BUTTONS", None)
        if instance_buttons:
            return instance_buttons

        if self.kwargs.get("pk", None):
            instance_buttons = ["refresh"]
        else:
            instance_buttons = ["reset"]

        ct = ContentType.objects.get_for_model(self.get_serializer_class().Meta.model)

        save_permission = f"{ct.app_label}.change_{ct.model}"
        delete_permission = f"{ct.app_label}.delete_{ct.model}"

        if request.user.has_perm(save_permission):
            instance_buttons.append("save")

        if request.user.has_perm(delete_permission) and self.kwargs.get("pk", None):
            instance_buttons.append("delete")

        return instance_buttons

    def get_preview_display(self, request: Request):
        return getattr(self, "PREVIEW_DISPLAY", "")

    def get_preview_buttons(self, request: Request):
        return [button.to_dict() for button in getattr(self, "PREVIEW_BUTTONS", [])]

    def get_custom_instance_buttons(self, request: Request):
        if "pk" in self.kwargs:
            return [
                button.to_dict()
                for button in getattr(self, "CUSTOM_INSTANCE_BUTTONS", [])
            ]
        else:
            return [
                button.to_dict()
                for button in getattr(self, "CUSTOM_LIST_INSTANCE_BUTTONS", [])
            ]

    def get_list_buttons(self, request):
        list_buttons = getattr(self, "LIST_BUTTONS", None)
        if list_buttons:
            return list_buttons

        list_buttons = ["refresh"]

        ct = ContentType.objects.get_for_model(self.get_serializer_class().Meta.model)
        permission = f"{ct.app_label}.add_{ct.model}"

        if request.user.has_perm(permission):
            list_buttons.append("new")

        return list_buttons

    # PAGINATION
    def get_pagination(self, request: Request):

        pagination = (
            self.pagination_class.__name__
            if hasattr(self, "pagination_class") and self.pagination_class
            else None
        )

        return {
            "CursorPagination": "cursor",
            "LimitOffsetPagination": "page",
            None: None,
        }[pagination]

    # TITLES

    def get_instance_widget_title(self, request: Request) -> str:
        return getattr(self, "INSTANCE_WIDGET_TITLE", "")

    def get_list_widget_title(self, request: Request) -> str:
        return getattr(self, "LIST_WIDGET_TITLE", "")

    def get_create_widget_title(self, request: Request) -> str:
        return getattr(self, "CREATE_WIDGET_TITLE", "")

    def get_titles(self, request: Request) -> Dict:
        return {
            "instance": self.get_instance_widget_title(request),
            "list": self.get_list_widget_title(request),
            "create": self.get_create_widget_title(request),
        }

    # Search, Ordering, Filter
    def get_search_fields(self, request: Request) -> Generator[str, None, None]:
        if filters.SearchFilter in self.filter_backends:
            yield from self.search_fields

    def get_ordering_fields(self, request: Request) -> Generator[str, None, None]:
        if filters.OrderingFilter in self.filter_backends:
            yield from self.ordering_fields

    def get_filter_fields(self, request: Request) -> Generator[Dict, None, None]:
        if DjangoFilterBackend in self.filter_backends:
            filterset_class = DjangoFilterBackend().get_filterset_class(self)

            if hasattr(filterset_class, "base_filters"):
                filterset = filterset_class.base_filters.items()
                combined_fields = dict()
                for name, field in filterset:
                    representation = field.get_representation(request, name)
                    combined_key = representation.get("combined_key", None)
                    if combined_key:
                        # If there is a combined key we need to check wether this is the first
                        # combined key we found. If not then we need to add this field together
                        # with the previously found combined key, clean up and yield it
                        if combined_key in combined_fields:
                            other_representation = combined_fields[combined_key]
                            for key in (
                                other_representation.keys() - representation.keys()
                            ):
                                representation[key] = other_representation[key]

                            del representation["combined_key"]
                            del combined_fields[combined_key]

                            yield combined_key, representation
                        else:
                            combined_fields[combined_key] = representation
                    else:
                        yield name, representation
