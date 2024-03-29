from rest_framework.reverse import reverse

from bridger import buttons as bt
from bridger import serializers
from bridger.serializers import BridgerType, register_dynamic_button, register_resource
from bridger.tags.serializers import TagSerializerMixin

from .models import ModelTest, RelatedModelTest


class ActionButtonSerializer(serializers.Serializer):

    char_field = serializers.CharField()
    custom_field = serializers.ChoiceField(choices=["a", "b"])


class ModelTestRepresentationSerializer(serializers.RepresentationSerializer):

    _detail = serializers.HyperlinkField(reverse_name="modeltest-detail")
    _detail_preview = serializers.HyperlinkField(reverse_name="modeltest-detail")

    filter_params = {"some_key": "some_value"}

    label_key = "{{|:-}}LEFT ALIGN{{|::}}CENTER{{|-:}}{{char_field}}"

    class Meta:
        model = ModelTest
        fields = ("id", "char_field", "_detail", "_detail_preview")


class RelatedModelTestRepresentationSerializer(serializers.RepresentationSerializer):

    _detail = serializers.HyperlinkField(reverse_name="relatedmodeltest-detail")

    class Meta:
        model = RelatedModelTest
        fields = ("id", "char_field", "_detail")


class ModelTestSerializer(TagSerializerMixin, serializers.ModelSerializer):

    _related_models = RelatedModelTestRepresentationSerializer(source="related_models", many=True)

    annotated_char_field = serializers.CharField(required=False, read_only=True)
    star_rating = serializers.StarRatingField()

    @register_dynamic_button()
    def something(self, instance, request, user):
        return [bt.HyperlinkButton(endpoint="https://www.google.com", icon="wb-icon-trash")]

    @register_resource()
    def related_models(self, instance, request, user):
        return {"related_model": reverse("relatedmodeltest-list", request=request)}

    @register_resource()
    def self_endpoint(self, instance, request, user):
        return {"self_endpoint": reverse("modeltest-detail", args=[instance.id], request=request)}

    class Meta:
        percent_fields = ["percent_field"]
        decorators = {
            "char_field": serializers.decorator(position="left", value="Decorator"),
            "integer_field": serializers.decorator(position="left", value="#"),
        }
        required_fields = ["choice_field"]

        model = ModelTest
        fields = (
            "id",
            "char_field",
            "text_field",
            "float_field",
            "integer_field",
            "percent_field",
            "decimal_field",
            "datetime_field",
            "datetime_field1",
            "date_field",
            "time_field",
            "boolean_field",
            "choice_field",
            "status_field",
            "image_field",
            "file_field",
            "related_models",
            "_related_models",
            "annotated_char_field",
            "star_rating",
            "_additional_resources",
            "_buttons",
            "tags",
            "_tags",
        )


class CalendarModelTestSerializer(ModelTestSerializer):
    class Meta:
        model = ModelTest
        fields = ("id", "char_field", "float_field", "integer_field","decimal_field", "percent_field", "datetime_field", "datetime_field1", "date_field", "time_field",
            "boolean_field", "choice_field", "star_rating",)


class RelatedModelTestSerializer(TagSerializerMixin, serializers.ModelSerializer):

    _model_test = ModelTestRepresentationSerializer(source="model_test")
    _model_tests = ModelTestRepresentationSerializer(source="model_tests", many=True)
    some_method_field = serializers.SerializerMethodField()
    text_json = serializers.JSONTextEditorField(required=False)
    text_markdown = serializers.TextField(label="text_json")
    # char_field = serializers.CharField(label="Char", secure=True)

    def get_some_method_field(self, obj):
        return obj.char_field.lower()

    @register_resource()
    def register_authenticated_html_page(self, instance, request, user):
        return {"html": reverse("relatedmodeltest-authenticated-html", args=[instance.id])}

    class Meta:
        required_fields = ["model_test", "model_tests"]
        model = RelatedModelTest
        fields = (
            "id",
            "char_field",
            "model_test",
            "_model_test",
            "model_tests",
            "_model_tests",
            "upper_char_field",
            "some_method_field",
            "text_json",
            "text_markdown",
            "tags",
            "_tags",
            "list_field",
            "_additional_resources",
        )
