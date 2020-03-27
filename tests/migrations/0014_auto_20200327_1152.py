# Generated by Django 2.2.11 on 2020-03-27 10:52

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0013_auto_20200219_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modeltest',
            name='status_field',
            field=django_fsm.FSMField(choices=[('status1', 'Status1'), ('status2', 'Status2'), ('status3', 'Status3')], default='status1', max_length=50, verbose_name='Status'),
        ),
    ]
