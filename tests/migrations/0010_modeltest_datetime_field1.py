# Generated by Django 2.2.9 on 2020-01-28 14:50

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tests", "0009_auto_20200113_1239"),
    ]

    operations = [
        migrations.AddField(
            model_name="modeltest",
            name="datetime_field1",
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
