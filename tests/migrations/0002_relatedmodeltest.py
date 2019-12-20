# Generated by Django 2.2.9 on 2019-12-20 04:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedModelTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('char_field', models.CharField(max_length=255)),
                ('model_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_models', to='tests.ModelTest')),
            ],
        ),
    ]
