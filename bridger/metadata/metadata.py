from rest_framework.metadata import BaseMetadata

from bridger.enums import WidgetType
from bridger.history.viewsets import get_historical_viewset

from .fields import (
    ButtonMetadata,
    CreateButtonMetadata,
    CustomButtonMetadata,
    CustomInstanceButtonMetadata,
    DocsMetadata,
    EndpointMetadata,
    FieldsMetadata,
    FilterFieldsMetadata,
    IdentifierMetadata,
    InstanceDisplayMetadata,
    ListDisplayMetadata,
    OrderingFieldsMetadata,
    PaginationMetadata,
    PKMetadata,
    PreviewMetadata,
    SearchFieldsMetadata,
    TitleMetadata,
    WidgetTypeMetadata,
)


class BridgerMetadata(BaseMetadata):
    def __init__(self, *args, **kwargs):
        self.modules = [
            IdentifierMetadata,
            WidgetTypeMetadata,
            TitleMetadata,
            EndpointMetadata,
            ButtonMetadata,
            CreateButtonMetadata,
            CustomButtonMetadata,
            CustomInstanceButtonMetadata,
            PaginationMetadata,
            SearchFieldsMetadata,
            OrderingFieldsMetadata,
            FilterFieldsMetadata,
            PreviewMetadata,
            # DocsMetadata,
        ]
        self.model_modules = [
            InstanceDisplayMetadata,
            ListDisplayMetadata,
            FieldsMetadata,
            PKMetadata,
        ]
        super().__init__(*args, **kwargs)

    def generate_metadata(self, request, view):
        for module in self.modules:
            yield from module(view, request)

    def generate_model_metadata(self, request, view):
        for module in self.model_modules:
            yield from module(view, request)

    def determine_metadata(self, request, view):
        # if view.historical_mode:
        #     format_kwarg = view.format_kwarg
        #     old_kwargs = view.kwargs

        #     model = type(view.get_object())
        #     historical_model = view.get_object().history.model

        #     view_class = get_historical_viewset(model, historical_model)
        #     view = view_class()
        #     view.kwargs = {"model_pk": old_kwargs["pk"]}
        #     view.request = request
        #     view.format_kwarg = format_kwarg

        metadata = dict(self.generate_metadata(request, view))

        if metadata["type"] in [WidgetType.INSTANCE.value, WidgetType.LIST.value]:
            metadata.update(dict(self.generate_model_metadata(request, view)))

        return metadata
