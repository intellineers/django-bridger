# Generated by Django 2.2.10 on 2020-02-18 12:29

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bridger', '0002_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='buttons',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True),
        ),
    ]
