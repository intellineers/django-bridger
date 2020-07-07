from rest_framework.request import Request

from bridger.enums import WidgetType
from bridger.metadata.mixins import BridgerMetadataMixin


class TitleMetadata(BridgerMetadataMixin):
    key = "titles"
    method_name = "_get_titles"


class TitleMetadataMixin:
    def get_instance_title(self, request: Request, title: str = None) -> str:
        if title:
            return title

        if hasattr(self, "get_serializer_class"):
            serializer_class = self.get_serializer_class()
            if hasattr(serializer_class, "Meta"):
                model = self.get_serializer_class().Meta.model

                if hasattr(model, "get_representation_label_key"):
                    return f"{model._meta.verbose_name}: {model.get_representation_label_key()}"

                return model._meta.verbose_name

        return ""

    def get_list_title(self, request: Request, title: str = None) -> str:
        if title:
            return title

        if hasattr(self, "get_serializer_class"):
            serializer_class = self.get_serializer_class()
            if hasattr(serializer_class, "Meta"):
                model = self.get_serializer_class().Meta.model
                return model._meta.verbose_name_plural

        return ""

    def get_create_title(self, request: Request, title: str = None) -> str:
        if title:
            return title

        if hasattr(self, "get_serializer_class"):
            serializer_class = self.get_serializer_class()
            if hasattr(serializer_class, "Meta"):
                model = self.get_serializer_class().Meta.model
                return f"Create {model._meta.verbose_name}"

        return ""

    def _get_titles(self, request: Request) -> str:
        return {
            "instance": self.get_instance_title(request, getattr(self, "INSTANCE_TITLE", None)),
            "list": self.get_list_title(request, getattr(self, "LIST_TITLE", None)),
            "create": self.get_create_title(request, getattr(self, "CREATE_TITLE", None)),
        }
