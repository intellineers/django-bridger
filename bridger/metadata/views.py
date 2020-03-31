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
    DocsMetadataMixin,
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
