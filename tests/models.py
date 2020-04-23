from datetime import date, time

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django_fsm import FSMField, transition
from rest_framework.reverse import reverse
from simple_history.models import HistoricalRecords

from bridger.buttons import ActionButton
from bridger.display import FieldSet, InstanceDisplay, Section
from bridger.enums import RequestType
from bridger.search import register as search_register


@search_register(endpoint="modeltest-list")
class ModelTest(models.Model):
    @classmethod
    def search_for_term(cls, search_term, request=None):
        return (
            cls.objects.all()
            .annotate(
                _search=models.functions.Concat(
                    models.F("char_field"),
                    models.Value(" "),
                    models.F("text_field"),
                    output_field=models.CharField(),
                )
            )
            .annotate(_repr=models.F("char_field"))
        )

    STATUS1 = "status1"
    STATUS2 = "status2"
    STATUS3 = "status3"
    status_choices = ((STATUS1, "Status1"), (STATUS2, "Status2"), (STATUS3, "Status3"))

    MOVE_BUTTON1 = ActionButton(
        method=RequestType.PATCH,
        icon="wb-icon-thumbs-up-full",
        key="move1",
        label="Move1",
        action_label="Move1",
        description_fields="<p>We will move1 this model.</p>",
        instance_display=InstanceDisplay(
            sections=[Section(fields=FieldSet(fields=["char_field", "integer_field"]))]
        ),
        identifiers=["tests:modeltest"],
    )

    MOVE_BUTTON2 = ActionButton(
        method=RequestType.PATCH,
        icon="wb-icon-thumbs-up-full",
        key="move2",
        label="Move2",
        action_label="Move2",
        description_fields="<p>We will move2 this model.</p>",
        instance_display=InstanceDisplay(
            sections=[Section(fields=FieldSet(fields=["char_field", "integer_field"]))]
        ),
        identifiers=["tests:modeltest"],
    )

    # Text
    char_field = models.CharField(max_length=255, verbose_name="Char")
    text_field = models.TextField(null=True, blank=True)

    # Numbers
    integer_field = models.IntegerField(verbose_name="Integer")
    float_field = models.FloatField()
    decimal_field = models.DecimalField(decimal_places=4, max_digits=7)
    percent_field = models.FloatField()

    # Date and Time
    datetime_field = models.DateTimeField(verbose_name="DateTime")
    datetime_field1 = models.DateTimeField(verbose_name="DateTime 1")
    date_field = models.DateField()
    time_field = models.TimeField()

    # Boolean
    boolean_field = models.BooleanField()

    star_rating = models.PositiveIntegerField()

    # Choice
    choice_field = models.CharField(
        max_length=64, choices=(("a", "A"), ("b", "B")), default="a"
    )

    # Status
    status_field = FSMField(
        default=STATUS1, choices=status_choices, verbose_name="Status"
    )

    # Files
    image_field = models.ImageField(null=True)
    file_field = models.FileField(null=True)

    history = HistoricalRecords()

    @transition(
        field=status_field,
        source=[STATUS1],
        target=STATUS2,
        custom={"_transition_button": MOVE_BUTTON1},
    )
    def move1(self):
        """Moves the model from Status1 to Status2"""
        pass

    @transition(
        field=status_field,
        source=[STATUS1, STATUS2],
        target=STATUS3,
        custom={"_transition_button": MOVE_BUTTON2},
    )
    def move2(self):
        """Moves the model from Status1 or Status2 to Status3"""
        pass

    @classmethod
    def get_endpoint_basename(cls):
        return "modeltest"

    @classmethod
    def get_endpoint(cls):
        return "modeltest-list"

    @classmethod
    def get_representation_endpoint(cls):
        return "modeltestrepresentation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{char_field}}"

    class Meta:
        verbose_name = "Test Model"
        verbose_name_plural = "Test Models"


@search_register(endpoint="relatedmodeltest-list")
class RelatedModelTest(models.Model):
    @classmethod
    def search_for_term(cls, request=None):
        return (
            cls.objects.all()
            .annotate(_search=models.F("char_field"))
            .annotate(_repr=models.F("char_field"))
        )

    text_json = JSONField(default=list, blank=True, null=True)
    text_markdown = models.TextField(default="")
    model_test = models.ForeignKey(
        to="tests.ModelTest",
        related_name="related_models",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Model Test",
    )
    model_tests = models.ManyToManyField(
        to="tests.ModelTest",
        related_name="related_models_m2m",
        blank=True,
        verbose_name="Model Tests1",
    )
    char_field = models.CharField(max_length=255, verbose_name="Char")

    history = HistoricalRecords()

    def __str__(self):
        return self.char_field

    @property
    def upper_char_field(self):
        return self.char_field.upper()

    @classmethod
    def get_endpoint_basename(cls):
        return "relatedmodeltest"

    @classmethod
    def get_representation_endpoint(cls):
        return "relatedmodeltestrepresentation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{char_field}}"

    class Meta:
        verbose_name = "Related Model Test"
        verbose_name_plural = "Related Model Tests"
