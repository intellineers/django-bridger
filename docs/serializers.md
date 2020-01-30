# Additional Resources

Additional Resources can be used for:

* List Instance Buttons
* Form Sections

Each additional resource has to be specified as a method decorated by `register_resource()` and has to accept `self`, `instance`, `request` and `user` as parameters. It needs to return a dictionairy.

Example:

```python
from bridger.serializers import ModelSerializer, register_resource

class SomeModelSerializer(ModelSerializer):

    @register_resource()
    def some_resource(self, instance, request, user):
        # Do some something (checks, etc.)
        return {
            "some-key": reverse("some-url", request=request)
        }
```