from typing import Optional

from bridger import display as dp
from bridger.display.metadata_config import DisplayConfig
from rest_framework.request import Request

class RelatedModelTestDisplayConfig(DisplayConfig):
   
    def get_instance_display(self) -> Optional[dp.InstanceDisplay]:
        return dp.InstanceDisplay(
            sections=[
                dp.Section(fields=dp.FieldSet(fields=["char_field", "tags", "model_test", "model_tests", "text_markdown"]))
            ]
        )

    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="char_field", label="Char1"),
                dp.Field(key="model_test", label="Model"),
                dp.Field(key="model_tests", label="Model(M2M)"),
                dp.Field(key="text_markdown", label="Markdown"),
                dp.Field(key="tags", label="Tags"),
            ]
        )
