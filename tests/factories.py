import factory

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
    integer_field = factory.Faker("pyint")
    datetime_field = factory.Faker("date_time")
    date_field = factory.Faker("date_object")
    time_field = factory.Faker("time_object")

    related_models = factory.RelatedFactory(
        "tests.factories.RelatedModelTestFactory", "model_test"
    )
