from bridger import buttons as bt
from bridger import display as dp
from bridger.enums import Unit
from bridger.messages import info
from bridger.serializers import ListSerializer
from bridger.viewsets import (
    ModelViewSet,
    RepresentationModelViewSet,
    ReadOnlyModelViewSet,
)

from tests.models import ModelTest, RelatedModelTest
from tests.serializers import (
    ActionButtonSerializer,
    RelatedModelTestRepresentationSerializer,
    RelatedModelTestSerializer,
)

from bridger.pagination import LimitOffsetPagination


class RelatedModelTestRepresentationViewSet(RepresentationModelViewSet):
    queryset = RelatedModelTest.objects.all()
    serializer_class = RelatedModelTestRepresentationSerializer


class RelatedModelTestModelViewSet(ModelViewSet):
    pagination_class = LimitOffsetPagination

    ENDPOINT = "relatedmodeltest-list"
    LIST_DISPLAY = dp.ListDisplay(
        fields=[
            dp.Field(key="char_field", label="Char", width=Unit.FRACTION(2)),
            dp.Field(key="model_test", label="Model", width=Unit.FRACTION(2)),
            dp.Field(key="model_tests", label="Model(M2M)", width=Unit.FRACTION(2)),
            dp.Field(key="text_markdown", label="Markdown", width=Unit.FRACTION(2)),
        ]
    )
    INSTANCE_DISPLAY = dp.InstanceDisplay(
        sections=[
            dp.Section(
                fields=dp.FieldSet(
                    fields=["char_field", "model_test", "model_tests", "text_markdown",]
                )
            )
        ]
    )
    CUSTOM_INSTANCE_BUTTONS = CUSTOM_LIST_INSTANCE_BUTTONS = [
        bt.DropDownButton(
            label="Dropdown",
            icon="wb-icon-triangle-down",
            buttons=[
                bt.DropDownButton(
                    label="Dropdown",
                    icon="wb-icon-triangle-down",
                    buttons=[
                        bt.ActionButton(
                            label="TestButton",
                            icon="wb-icon-trash",
                            endpoint="http://localhost:5000/relatedmodeltest/",
                            instance_display=dp.InstanceDisplay(
                                sections=[
                                    dp.Section(
                                        fields=dp.FieldSet(
                                            fields=["char_field", "custom_field"]
                                        )
                                    ),
                                ]
                            ),
                            serializer=ActionButtonSerializer,
                        ),
                        bt.HyperlinkButton(
                            endpoint="https://www.google.com", icon="wb-icon-trash",
                        ),
                    ],
                ),
            ],
        )
    ]

    filter_fields = {"model_test": ["exact"], "char_field": ["exact"]}
    search_fields = ["char_field"]
    ordering_fields = ["id", "model_test__char_field"]
    queryset = RelatedModelTest.objects.all()
    serializer_class = RelatedModelTestSerializer

    def get_messages(self, instance=None, initial=None, **kwargs):
        if instance:
            return [info("This is an instance message.")]
        if initial:
            return [info("This is a list message")]

    def get_serializer_changes(self, serializer):
        if not isinstance(serializer, ListSerializer) and hasattr(serializer, "fields"):
            if "model_tests" in serializer.fields:
                default_values = ModelTest.objects.all()[:3].values_list(
                    "id", flat=True
                )
                serializer.fields["model_tests"].child_relation.default = default_values
        return serializer
