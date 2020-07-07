import pathlib
import uuid

from django.db import models
from django.dispatch import receiver


class Asset(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    file = models.FileField(upload_to="markdown/assets")
    content_type = models.CharField(max_length=10, null=True, blank=True)
    file_url_name = models.CharField(max_length=1024, null=True, blank=True)
    # public = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"


@receiver(models.signals.pre_save, sender="bridger.Asset")
def generate_content_type(sender, instance, **kwargs):
    if suffix := pathlib.Path(instance.file.name).suffix:
        instance.content_type = suffix[1:]
        instance.file_url_name = f"{instance.id}{suffix}"
