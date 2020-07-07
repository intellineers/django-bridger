Since one app can impose indirect dependencies to other apps by adding buttons to their views, django bridger defines two signals to remedy this and to provide means to define buttons and resources outside of an app:

### add_instance_buttons

To add an instance button into a remote app, simply create a receiver which listens to the `bridger.signals.instance_buttons.add_instance_button` signal and which acceps the following arguments:

* sender: The Viewset class that is sending the signal
* many: Boolean, indicates whether it is a list or an instance

Example:

```python
@receiver(add_instance_button, sender=<ModelViewSet>)
def add_instance_buttons_receiver(sender, many, *args, **kwargs):
    return bt.HyperlinkButton(icon="<icon>", label="<label>", endpoint="<url>")
```

Sometimes you wan to create a button with a key instead of an endpoint, where the key is an additional resource.

### add_additional_resources

To add an additional resource to a remote app, create a receiver which listens to the `bridger.signals.instance_buttons.add_additional_resouce` and which accepts the following arguments:

* sender: The Serializer Class that is sending the signal
* serializer: The Serializer instance that is sending the signal
* request: The current request
* user: The current user

Example:

```python
@receiver(add_additional_resource, sender=<ModelSerializer>)
def test_adding_additional_resource(sender, serializer, instance, request, user, **kwargs):
    return {"<key>": "<url>"}
```