from .fields import (
    ButtonMetadataMixin,
    CreateButtonMetadataMixin,
    CustomButtonMetadataMixin,
    CustomInstanceButtonMetadataMixin,
    DocsMetadataMixin,
    EndpointMetadataMixin,
    FieldsMetadataMixin,
    FilterFieldsMetadataMixin,
    IdentifierMetadataMixin,
    InstanceDisplayMetadataMixin,
    ListDisplayMetadataMixin,
    OrderingFieldsMetadataMixin,
    PaginationMetadataMixin,
    PKMetadataMixin,
    PreviewMetadataMixin,
    SearchFieldsMetadataMixin,
    TitleMetadataMixin,
    WidgetTypeMetadataMixin,
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
    DocsMetadataMixin,
):
    metadata_class = BridgerMetadata
