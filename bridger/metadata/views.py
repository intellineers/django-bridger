from bridger.buttons.metadata_config import ButtonConfigMixin
from bridger.display.metadata_config import DisplayConfigMixin
from bridger.titles.metadata_config import TitleConfigMixin

from .metadata import BridgerMetadata


class MetadataMixin(DisplayConfigMixin, TitleConfigMixin, ButtonConfigMixin):
    metadata_class = BridgerMetadata
