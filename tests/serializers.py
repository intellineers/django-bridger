from bridger import serializers
from .models import ModelTest, RelatedModelTest


class ModelTestRepresentationSerializer(serializers.RepresentationSerializer):

    value_key = "id"
    label_key = "{{char_field}}"
    endpoint = "modeltestrepresentation-list"

    _detail = serializers.HyperlinkField(reverse_name="modeltest-detail")

    class Meta:
        model = ModelTest
        fields = ("id", "char_field", "_detail")


class ModelTestSerializer(serializers.ModelSerializer):
    class Meta:
        percent_fields = ["percent_field"]
        decorators = {
            "char_field": serializers.decorator(position="left", value="Decorator"),
        }

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
            "date_field",
            "time_field",
            "boolean_field",
            "choice_field",
            "status_field",
            "image_field",
            "file_field",
            "_additional_resources",
        )


class RelatedModelTestSerializer(serializers.ModelSerializer):

    _model_test = ModelTestRepresentationSerializer(source="model_test")

    class Meta:
        model = RelatedModelTest
        fields = ("id", "char_field", "model_test", "_model_test")
