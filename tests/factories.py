import factory
import pytz
from django.conf import settings
from factory.fuzzy import FuzzyChoice
from faker import Faker

from .models import ModelTest, RelatedModelTest


class RelatedModelTestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RelatedModelTest

    char_field = factory.Faker("pystr", min_chars=5, max_chars=20)
    model_test = factory.SubFactory("tests.factories.ModelTestFactory")


class ModelTestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ModelTest

    char_field = factory.Faker("pystr", min_chars=5, max_chars=20)
    float_field = factory.Faker("pyfloat")
    percent_field = factory.Faker(
        "pyfloat", left_digits=0, right_digits=4, positive=True,
    )
    integer_field = factory.Faker("pyint")
    star_rating = factory.Faker("pyint", min_value=1, max_value=5)
    decimal_field = factory.Faker("pydecimal", left_digits=3, right_digits=4)
    datetime_field = pytz.timezone(settings.TIME_ZONE).localize(Faker().date_time())
    datetime_field1 = pytz.timezone(settings.TIME_ZONE).localize(Faker().date_time())
    date_field = factory.Faker("date_object")
    time_field = factory.Faker("time_object")
    boolean_field = factory.Faker("pybool")
    choice_field = FuzzyChoice(choices=["a", "b"])
    related_models = factory.RelatedFactory(
        "tests.factories.RelatedModelTestFactory", "model_test"
    )
