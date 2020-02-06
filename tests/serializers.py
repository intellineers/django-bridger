from rest_framework.reverse import reverse

from bridger import serializers
from bridger.serializers import register_resource

from .models import ModelTest, RelatedModelTest


class ModelTestRepresentationSerializer(serializers.RepresentationSerializer):

    _detail = serializers.HyperlinkField(reverse_name="modeltest-detail")
    _detail_preview = serializers.HyperlinkField(reverse_name="modeltest-detail")

    class Meta:
        model = ModelTest
        fields = ("id", "char_field", "_detail", "_detail_preview")


class ModelTestSerializer(serializers.ModelSerializer):
    @register_resource()
    def related_models(self, instance, request, user):
        return {"related_model": reverse("relatedmodeltest-list", request=request)}

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
            "datetime_field1",
            "date_field",
            "time_field",
            "boolean_field",
            "choice_field",
            "status_field",
            "image_field",
            "file_field",
            "_additional_resources",
        )


class CalendarModelTestSerializer(ModelTestSerializer):
    class Meta:
        model = ModelTest
        fields = ("id", "char_field", "datetime_field", "datetime_field1")


class RelatedModelTestSerializer(serializers.ModelSerializer):

    _model_test = ModelTestRepresentationSerializer(source="model_test")

    class Meta:
        model = RelatedModelTest
        fields = ("id", "char_field", "model_test", "_model_test")
