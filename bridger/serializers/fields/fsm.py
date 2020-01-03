from bridger.serializers.fields.text import CharField
from bridger.serializers.fields.choice import ChoiceField


# TODO: Color for each state
class FSMStatusField(CharField):

    field_type = "status"

    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop("choices")
        super().__init__(read_only=True, *args, **kwargs)

    def get_representation(self, request, field_name):
        representation = super().get_representation(request, field_name)
        representation["choices"] = list()
        model = self.parent.Meta.model

        for choice in self.choices:
            representation["choices"].append({"value": choice[0], "label": choice[1]})

        return representation