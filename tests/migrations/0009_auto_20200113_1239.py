# Generated by Django 2.2.9 on 2020-01-13 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0008_modeltest_text_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='modeltest',
            name='file_field',
            field=models.FileField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='modeltest',
            name='image_field',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
