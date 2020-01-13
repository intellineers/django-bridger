from datetime import date, time

from django.db import models
from django.utils import timezone
from django_fsm import FSMField, transition

from bridger.fsm.buttons import FSMButton
from bridger.display import InstanceDisplay, Section, FieldSet


class ModelTest(models.Model):

    STATUS1 = "status1"
    STATUS2 = "status2"
    STATUS3 = "status3"
    status_choices = ((STATUS1, "Status1"), (STATUS2, "Status2"), (STATUS3, "Status3"))

    MOVE_BUTTON1 = FSMButton(
        icon="wb-icon-thumbs-up-full",
        key="move1",
        label="Move1",
        action_label="Move1",
        description_fields=["We will move1 this model."],
        instance_display=InstanceDisplay(
            sections=[Section(fields=FieldSet(fields=["char_field", "integer_field"]))]
        ),
    )

    MOVE_BUTTON2 = FSMButton(
        icon="wb-icon-thumbs-up-full",
        key="move2",
        label="Move2",
        action_label="Move2",
        description_fields=["We will move2 this model."],
        instance_display=InstanceDisplay(
            sections=[Section(fields=FieldSet(fields=["char_field", "integer_field"]))]
        ),
    )

    char_field = models.CharField(max_length=255, verbose_name="Char")
    integer_field = models.IntegerField()
    float_field = models.FloatField()
    percent_field = models.FloatField()
    datetime_field = models.DateTimeField()
    date_field = models.DateField()
    time_field = models.TimeField()

    boolean_field = models.BooleanField()
    choice_field = models.CharField(
        max_length=64, choices=(("a", "A"), ("b", "B")), default="a"
    )

    status_field = FSMField(default=STATUS1, choices=status_choices)

    @transition(
        field=status_field,
        source=[STATUS1],
        target=STATUS2,
        custom={"_transition_button": MOVE_BUTTON1},
    )
    def move1(self):
        pass

    @transition(
        field=status_field,
        source=[STATUS2],
        target=STATUS3,
        custom={"_transition_button": MOVE_BUTTON2},
    )
    def move2(self):
        pass

    class Meta:
        verbose_name = "Test Model"
        verbose_name_plural = "Test Models"


class RelatedModelTest(models.Model):

    model_test = models.ForeignKey(
        to="tests.ModelTest", related_name="related_models", on_delete=models.CASCADE
    )
    char_field = models.CharField(max_length=255)
