from django.db import models
from django.db.models.fields.reverse_related import ManyToManyRel
from django.db.models.query import QuerySet


class Tag(models.Model):
    title = models.CharField(max_length=255, unique=True)
    color = models.CharField(max_length=7, default="#D3D3D3")

    @classmethod
    def get_representation_endpoint(cls):
        return "bridger:tagrepresentation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{title}}"

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def get_tagged_queryset(self):
        qs = self.__class__.objects.none()
        for field in filter(lambda x: isinstance(x, ManyToManyRel), self.__class__._meta.get_fields()):
            _qs = getattr(self, field.related_name).all()
            qs = qs.union(_qs.values("tag_detail_endpoint", "tag_representation"))
        return qs


class TagModelMixin(models.Model):

    tag_detail_endpoint = models.CharField(max_length=255, null=True, blank=True)
    tag_representation = models.CharField(max_length=255, null=True, blank=True)

    tags = models.ManyToManyField(to="bridger.Tag", related_name="%(app_label)s_%(class)s_items", blank=True)

    def save(self, *args, **kwargs):
        self.tag_detail_endpoint = self.get_tag_detail_endpoint()
        self.tag_representation = self.get_tag_representation()
        super().save(*args, **kwargs)

    def get_tag_detail_endpoint(self):
        raise NotImplementedError("When using Tags, you must implement get_tag_detail_endpoint")

    def get_tag_representation(self):
        raise NotImplementedError("When using Tags, you must implement get_tag_representation")

    class Meta:
        abstract = True
