import pytest
from .mixins import TestModelClass, TestSerializerClass, TestrepresentationViewSetClass, TestViewSetClass
from .utils import get_all_subclasses
from bridger import serializers
from bridger import viewsets
from django.db import models
from django.urls import get_resolver
get_resolver().url_patterns

models = filter(lambda x: not x.__module__.startswith(('bridger', 'django', 'rest_framework')), get_all_subclasses(models.Model))
serializers = filter(lambda x: "bridger" not in x.__module__, get_all_subclasses(serializers.ModelSerializer))
representationviewsets = filter(lambda x: "bridger" not in x.__module__, get_all_subclasses(viewsets.RepresentationViewSet))
modelviewsets = filter(lambda x: "bridger" not in x.__module__, get_all_subclasses(viewsets.ModelViewSet))

@pytest.mark.django_db 
class TestProject:
    @pytest.mark.parametrize("model", models)
    def test_models(self, model):
        # print(mvs.__name__)
        # print(mvs.__module__)
        my_test = TestModelClass(model)
        my_test.execute_test()

    @pytest.mark.parametrize("serializer", serializers)
    def test_serializers(self, serializer):
        my_test = TestSerializerClass(serializer)
        my_test.execute_test()

    @pytest.mark.parametrize("rvs", representationviewsets)
    def test_representationviewsets(self, rvs, admin_client):
        my_test = TestrepresentationViewSetClass(rvs)
        my_test.execute_test(admin_client)

    @pytest.mark.parametrize("mvs", modelviewsets)
    def test_modelviewsets(self, mvs, admin_client):
        my_test = TestViewSetClass(mvs)
        my_test.execute_test(admin_client)