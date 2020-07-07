from bridger import filters

from .models import Tag


class TagFilterMixin(filters.FilterSet):

    tags = filters.ModelMultipleChoiceFilter(
        endpoint="bridger:tagrepresentation-list", value_key="id", label_key="title", queryset=Tag.objects.all(),
    )
