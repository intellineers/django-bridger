from bridger.serializers import ModelSerializer, RepresentationSerializer
from .models import ModelTest


class ModelTestSerializer(ModelSerializer):
    class Meta:
        model = ModelTest
        fields = ("id", "char_field", "datetime_field", "date_field", "time_field")
