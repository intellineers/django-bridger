from pytest_factoryboy import register

from tests.factories import ModelTestFactory, RelatedModelTestFactory

register(RelatedModelTestFactory)
register(ModelTestFactory)
