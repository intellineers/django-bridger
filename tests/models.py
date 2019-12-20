from datetime import date, time

from django.db import models
from django.utils import timezone


class ModelTest(models.Model):

    char_field = models.CharField(max_length=255)
    integer_field = models.IntegerField()
    float_field = models.FloatField()
    percent_field = models.FloatField()
    datetime_field = models.DateTimeField()
    date_field = models.DateField()
    time_field = models.TimeField()

    class Meta:
        verbose_name = "Test Model"
        verbose_name_plural = "Test Models"


class RelatedModelTest(models.Model):

    model_test = models.ForeignKey(
        to="tests.ModelTest", related_name="related_models", on_delete=models.CASCADE
    )
    char_field = models.CharField(max_length=255)
