from bridger.buttons.metadata_config import ButtonConfigMixin
from bridger.display.metadata_config import DisplayConfigMixin
from bridger.titles.metadata_config import TitleConfigMixin
from bridger.endpoints.metadata_config import EndpointConfigMixin
from bridger.preview.metadata_config import PreviewConfigMixin

from .metadata import BridgerMetadata


class MetadataMixin(DisplayConfigMixin, EndpointConfigMixin, TitleConfigMixin, ButtonConfigMixin, PreviewConfigMixin):
    metadata_class = BridgerMetadata
