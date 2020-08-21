from typing import Optional

from bridger import display as dp
from bridger.display.metadata_config import DisplayConfig
from rest_framework.request import Request

class PandasDisplayConfig(DisplayConfig):
   
    def get_list_display(self) -> Optional[dp.ListDisplay]:
        return dp.ListDisplay(
            fields=[
                dp.Field(key="char_field", label="Char"),
                dp.Field(key="integer_field", label="Integer"),
                dp.Field(key="integer_annotated", label="Integer Anno"),
            ],
        )
