from slugify import slugify

from bridger.metadata import BridgerMetadata


class PandasMetadata(BridgerMetadata):
    def determine_metadata(self, request, view):
        metadata = super().determine_metadata(request, view)
        metadata["identifier"] += f"-{slugify(view.__class__.__name__)}"
        metadata["fields"] = view.pandas_fields.to_dict()
        return metadata
