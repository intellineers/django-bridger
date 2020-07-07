# Generated by Django 3.0.5 on 2020-05-07 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tests", "0021_auto_20200422_1410"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalmodeltest", name="integer_field", field=models.IntegerField(verbose_name="Integer"),
        ),
        migrations.AlterField(model_name="modeltest", name="integer_field", field=models.IntegerField(verbose_name="Integer"),),
        migrations.AlterField(
            model_name="relatedmodeltest",
            name="model_tests",
            field=models.ManyToManyField(
                blank=True, related_name="related_models_m2m", to="tests.ModelTest", verbose_name="Model Tests1",
            ),
        ),
    ]
