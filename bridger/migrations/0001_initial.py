# Generated by Django 2.2.9 on 2020-01-02 02:04

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FrontendUserConfiguration',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('config', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
                ('parent_configuration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_configurations', to='bridger.FrontendUserConfiguration')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='configurations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Frontend User Settings',
                'verbose_name_plural': 'Frontend User Settings',
            },
        ),
    ]
