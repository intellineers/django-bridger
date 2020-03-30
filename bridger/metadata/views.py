from .fields import (
    ButtonMetadataMixin,
    CreateButtonMetadataMixin,
    CustomButtonMetadataMixin,
    CustomInstanceButtonMetadataMixin,
    EndpointMetadataMixin,
    FieldsMetadataMixin,
    FilterFieldsMetadataMixin,
    IdentifierMetadataMixin,
    InstanceDisplayMetadataMixin,
    ListDisplayMetadataMixin,
    OrderingFieldsMetadataMixin,
    PaginationMetadataMixin,
    PKMetadataMixin,
    SearchFieldsMetadataMixin,
    TitleMetadataMixin,
    WidgetTypeMetadataMixin,
    PreviewMetadataMixin,
)
from .metadata import BridgerMetadata


class MetadataMixin(
    InstanceDisplayMetadataMixin,
    ListDisplayMetadataMixin,
    IdentifierMetadataMixin,
    WidgetTypeMetadataMixin,
    EndpointMetadataMixin,
    ButtonMetadataMixin,
    CreateButtonMetadataMixin,
    CustomButtonMetadataMixin,
    CustomInstanceButtonMetadataMixin,
    PaginationMetadataMixin,
    TitleMetadataMixin,
    SearchFieldsMetadataMixin,
    OrderingFieldsMetadataMixin,
    FilterFieldsMetadataMixin,
    FieldsMetadataMixin,
    PKMetadataMixin,
    PreviewMetadataMixin,
):
    metadata_class = BridgerMetadata
