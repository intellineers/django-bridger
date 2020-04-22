# Generated by Django 3.0.5 on 2020-04-16 08:49

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0017_auto_20200416_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalrelatedmodeltest',
            name='text_json',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='relatedmodeltest',
            name='text_json',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=list),
        ),
    ]