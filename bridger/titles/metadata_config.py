from typing import Optional

from rest_framework.request import Request
from bridger.metadata.mixins import BridgerViewSetConfig


class TitleConfig(BridgerViewSetConfig):
    def get_instance_title(self) -> str:
        name = self.view.get_model()._meta.verbose_name

        if self.instance:
            return f"{name}: {str(self.view.get_object())}"
        return name

    def get_delete_title(self) -> str:
        name = self.view.get_model()._meta.verbose_name

        if self.instance:
            return f"Delete {name}: {str(self.view.get_object())}"
        return f"Delete {name}"

    def get_list_title(self) -> str:
        return self.view.get_model()._meta.verbose_name_plural

    def get_create_title(self) -> str:
        return f"Create {self.view.get_model()._meta.verbose_name}"

    def get_metadata(self):
        yield "instance", self.get_instance_title()
        yield "list", self.get_list_title()
        yield "create", self.get_create_title()
        yield "delete", self.get_delete_title()

    @classmethod
    def get_metadata_key(cls):
        return "titles"

    @classmethod
    def get_metadata_fieldname(cls):
        return "title_config_class"


class TitleConfigMixin:
    title_config_class = TitleConfig
