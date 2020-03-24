# Generated by Django 2.2.9 on 2020-01-13 09:53

import django_fsm
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tests", "0004_modeltest_status_field"),
    ]

    operations = [
        migrations.AddField(
            model_name="modeltest",
            name="boolean_field",
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="modeltest",
            name="choice_field",
            field=models.CharField(
                choices=[("A", "a"), ("B", "b")], default="a", max_length=64
            ),
        ),
        migrations.AlterField(
            model_name="modeltest",
            name="char_field",
            field=models.CharField(max_length=255, verbose_name="Char"),
        ),
        migrations.AlterField(
            model_name="modeltest",
            name="status_field",
            field=django_fsm.FSMField(
                choices=[
                    ("status1", "Status1"),
                    ("status2", "Status2"),
                    ("status3", "Status3"),
                ],
                default="status1",
                max_length=50,
            ),
        ),
    ]
