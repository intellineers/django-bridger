# Generated by Django 2.2.12 on 2020-04-16 07:27

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0016_historicalrelatedmodeltest'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalrelatedmodeltest',
            name='text_json',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='relatedmodeltest',
            name='text_json',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]
