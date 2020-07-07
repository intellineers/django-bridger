from django.dispatch import receiver

from bridger import buttons as bt
from bridger.signals.instance_buttons import add_additional_resource, add_instance_button
from tests.serializers import RelatedModelTestSerializer
from tests.viewsets import RelatedModelTestModelViewSet


@receiver(add_instance_button, sender=RelatedModelTestModelViewSet)
def test_adding_instance_buttons_ep(sender, many, *args, **kwargs):
    return bt.HyperlinkButton(icon="wb-icon-trash", label="Far away button (EP)", endpoint="https://www.google.com")


@receiver(add_instance_button, sender=RelatedModelTestModelViewSet)
def test_adding_instance_buttons_key(sender, many, *args, **kwargs):
    return bt.HyperlinkButton(icon="wb-icon-trash", label="Far away button (KEY)", key="some-key")


@receiver(add_additional_resource, sender=RelatedModelTestSerializer)
def test_adding_additional_resource(sender, serializer, instance, request, user, **kwargs):
    return {"some-key": "https://www.google.com"}
