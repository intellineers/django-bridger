from rest_framework.metadata import BaseMetadata

from bridger.enums import WidgetType

from .fields import (
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
        metadata = dict(self.generate_metadata(request, view))

        if metadata["type"] in [WidgetType.INSTANCE.value, WidgetType.LIST.value]:
            metadata.update(dict(self.generate_model_metadata(request, view)))

        return metadata
