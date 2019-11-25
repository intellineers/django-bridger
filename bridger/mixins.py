from .metadata import BridgerMetaData
from django.contrib.contenttypes.models import ContentType
from rest_framework.reverse import reverse


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
    
    - instance_buttons: Default buttons which are displayed for an instance
       - Options: [save, save_and_new, save_and_close, delete, refresh]
    - custom_instance_buttons: Custom buttons which are displayed for an instance
    - list_buttons: Default buttons which are displayed for a list
       - Options: [refresh, new]
    - custom_list_buttons: Custom buttons which are displayed for a list
    - custom_list_instance_buttons: Custom buttons which are displayed for each entry
       in a list

    === MESSAGES ===
    Messages that should be conveyed through the OPTIONS request

    === DISPLAY ===
    The displays describe how a list or an instance should be displayed. Essentially,
    they describe a table layout for lists and a form for instances.

    === FORMAT ===
    TODO

    === LEGEND ===
    TODO

    === WIDGET TITLE ===
    TODO

    """

    metadata_class = BridgerMetaData

    # IDENTIFIER
    def get_identifier(self, request):
        identifier = getattr(self, "IDENTIFIER", None)
        if not identifier:
            ct = ContentType.objects.get_for_model(
                self.get_serializer_class().Meta.model
            )
            return f"{ct.app_label}:{ct.model}"
        return identifier

    # ENDPOINT
    def get_list_endpoint(self, request):
        endpoint = getattr(self, "LIST_ENDPOINT", None)
        if endpoint:
            return reverse(endpoint, request=request)

    def get_instance_endpoint(self, request):
        endpoint = getattr(self, "INSTANCE_ENDPOINT", None)
        if endpoint:
            return reverse(endpoint, request=request)

    def get_new_instance_endpoint(self, request):
        endpoint = getattr(self, "NEW_INSTANCE_ENDPOINT", None)
        if endpoint:
            return reverse(endpoint, request=request)

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

    def get_custom_instance_buttons(self, request):
        return getattr(self, "CUSTOM_INSTANCE_BUTTONS", list())

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

    def get_custom_list_buttons(self, request):
        return getattr(self, "CUSTOM_LIST_BUTTONS", list())

    def get_custom_list_instance_buttons(self, request):
        return getattr(self, "CUSTOM_LIST_INSTANCE_BUTTONS", list())

    # MESSAGES
    def get_messages(self, request):
        return getattr(self, "MESSAGES", [])

    # get displays
    def get_instance_display(self, request):
        if hasattr(self, "INSTANCE_DISPLAY"):
            return self.INSTANCE_DISPLAY

        fields = [{"fields": list()}]

        # for field_name, field in self.get_serializer().fields.items():
        #     if "_" != field_name[0] and not isinstance(
        #         field, wb_serializers.PrimaryKeyField
        #     ):
        #         fields[0]["fields"].append(field_name)
        return fields

    def get_list_display(self, request):
        if hasattr(self, "LIST_DISPLAY"):
            return self.LIST_DISPLAY

        fields = list()

        # for field_name, field in self.get_serializer().fields.items():
        #     if "_" != field_name[0] and not isinstance(
        #         field, wb_serializers.PrimaryKeyField
        #     ):
        #         fields.append({"key": field_name, "label": field.label})
        return fields

    def get_chart_display(self):
        return getattr(self, "CHART_DISPLAY", None)

    def get_calendar_display(self):
        return getattr(self, "IS_CALENDAR", False)

    def get_list_formatting(self, request):
        return getattr(self, "LIST_FORMATTING", None)

    def get_cell_formatting(self, request):
        return getattr(self, "CELL_FORMATTING", None)

    def get_legends(self, request):
        return getattr(self, "LEGENDS", None)

    # get titles
    def get_instance_widget_title(self):
        if hasattr(self, "INSTANCE_WIDGET_TITLE"):
            return self.INSTANCE_WIDGET_TITLE
        return f"{self.get_serializer_class().Meta.model._meta.verbose_name}"

    def get_new_instance_widget_title(self):
        if hasattr(self, "NEW_INSTANCE_WIDGET_TITLE"):
            return self.NEW_INSTANCE_WIDGET_TITLE
        return f"New {self.get_serializer_class().Meta.model._meta.verbose_name}"

    def get_list_widget_title(self):
        if hasattr(self, "LIST_WIDGET_TITLE"):
            return self.LIST_WIDGET_TITLE
        return f"{self.get_serializer_class().Meta.model._meta.verbose_name_plural}"
