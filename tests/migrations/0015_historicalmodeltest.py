# Generated by Django 2.2.12 on 2020-04-02 15:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_fsm
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tests', '0014_auto_20200327_1152'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalModelTest',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('char_field', models.CharField(max_length=255, verbose_name='Char')),
                ('text_field', models.TextField(blank=True, null=True)),
                ('integer_field', models.IntegerField()),
                ('float_field', models.FloatField()),
                ('decimal_field', models.DecimalField(decimal_places=4, max_digits=7)),
                ('percent_field', models.FloatField()),
                ('datetime_field', models.DateTimeField(verbose_name='DateTime')),
                ('datetime_field1', models.DateTimeField(verbose_name='DateTime 1')),
                ('date_field', models.DateField()),
                ('time_field', models.TimeField()),
                ('boolean_field', models.BooleanField()),
                ('choice_field', models.CharField(choices=[('a', 'A'), ('b', 'B')], default='a', max_length=64)),
                ('status_field', django_fsm.FSMField(choices=[('status1', 'Status1'), ('status2', 'Status2'), ('status3', 'Status3')], default='status1', max_length=50, verbose_name='Status')),
                ('image_field', models.TextField(max_length=100, null=True)),
                ('file_field', models.TextField(max_length=100, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Test Model',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
