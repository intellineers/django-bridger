from .fields import (
    ButtonMetadataMixin,
    CreateButtonMetadataMixin,
    CustomButtonMetadataMixin,
    CustomInstanceButtonMetadataMixin,
    EndpointMetadataMixin,
    IdentifierMetadataMixin,
    PaginationMetadataMixin,
    WidgetTypeMetadataMixin,
    TitleMetadataMixin,
    SearchFieldsMetadataMixin,
    OrderingFieldsMetadataMixin,
    FilterFieldsMetadataMixin,
    InstanceDisplayMetadataMixin,
    ListDisplayMetadataMixin,
    FieldsMetadataMixin,
    PKMetadataMixin,
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
):
    metadata_class = BridgerMetadata
