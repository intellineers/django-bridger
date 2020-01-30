All the serializers are build on top of Django Rest Framework. Basically there are two different Serializers, the `ModelSerializer` and `RepresentationSerializer`.

# Model Serializer

The base serializer, which is used for a standart django model. If the model has nothing special about it the application of the serializer is the same as the normal Django Rest Framework ModelSerializer:

```python
from bridger.serializers import ModelSerializer

class SomeModelSerializer(ModelSerializer):
    class Meta:
        model = SomeModel
        fields = "__all__"
```

Each field of `SomeModel` is automatically converted into a subclass of the respective Django Rest Framework field.

# Representation Serializer

The serializer for representing related models. The most basic example of this serializer is:

```python
from bridger.serializers import RepresentationSerializer, HyperlinkField

class SomeOtherModelRepresentationSerializer(RepresentationSerializer):

    value_key = "id"
    label_key = "{{some_field}}"
    endpoint = "someothermodel-representation-list"

    _detail = HyperlinkField(reverse_name="someothermodel-list")
    _detail_preview = HyperlinkField(reverse_name="someothermodel-list")

    class Meta:
        model = SomeOtherModel
        fields = ("id", "some_field", "_detail")
```

- **value_key**: The field which is used to identify the model, usually `id`.
- **label_key**: The fields which are used to represent the model as a handlebar string.
- **endpoint**: The endpoint to retrieve the representations. Used for async select fields and filters.
- **_detail**: If specified, the endpoint where a full version of this model can be found. Used for links in tables.
- **_detail_preview**: TODO

This `RepresentationSerializer` can be used in a `ModelSerializer`:

```python
class SomeModelSerializer(ModelSerializer):
    _some_other_model = SomeOtherModelRepresentationSerializer(source="some_other_model")
    class Meta:
        model = SomeModel
        fields = ["id", "some_other_model", "_some_other_model"]
```

# Additional Resources

Additional Resources can be used for:

* List Instance Buttons
* Form Sections

Each additional resource has to be specified as a method decorated by `register_resource()` and has to accept `self`, `instance`, `request` and `user` as parameters. It needs to return a dictionairy.

Example:

```python
from bridger.serializers import ModelSerializer, register_resource

class SomeModelSerializer(ModelSerializer)
    @register_resource()
    def some_resource(self, instance, request, user):
        # Do some something (checks, etc.)
        return {
            "some-key": reverse("some-url", request=request)
        }
```