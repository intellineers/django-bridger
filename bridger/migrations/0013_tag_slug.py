# Generated by Django 3.0.14 on 2021-05-10 08:48

from slugify import slugify
from django.db import migrations, models


def populate_slug_field(apps, schema_editor):
    Tag = apps.get_model("bridger", "Tag")
    for tag in Tag.objects.all():
        tag.slug = slugify(tag.title)
        tag.save()


class Migration(migrations.Migration):

    dependencies = [
        ('bridger', '0012_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.RunPython(populate_slug_field),
    ]
