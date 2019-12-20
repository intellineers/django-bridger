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
        model = ModelTest
        fields = ("id", "char_field", "datetime_field", "date_field", "time_field")


class RelatedModelTestSerializer(serializers.ModelSerializer):

    _model_test = ModelTestRepresentationSerializer(source="model_test")

    class Meta:
        model = RelatedModelTest
        fields = ("id", "char_field", "model_test", "_model_test")
