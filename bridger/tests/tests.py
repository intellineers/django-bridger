
import pytest
from bridger.tests.mixins import TestModelClass, TestSerializerClass, TestrepresentationViewSetClass, TestViewSetClass, TestInfViewSetClass
from bridger.tests.utils import get_all_subclasses, is_intermediate_table_m2m, all_subclasses
from bridger.tests.signals import get_specfics_module
from bridger import serializers
from bridger import viewsets
from django.db import models
from django.urls import get_resolver
get_resolver().url_patterns

models = filter(lambda x: not x.__module__.startswith(('bridger', 'django', 'rest_framework', 'dynamic_preferences', 'eventtools')) 
                and not x._meta.abstract and not is_intermediate_table_m2m(x), get_all_subclasses(models.Model))
serializers = filter(lambda x: "bridger" not in x.__module__, get_all_subclasses(serializers.ModelSerializer))
representationviewsets = filter(lambda x: "bridger" not in x.__module__, get_all_subclasses(viewsets.RepresentationViewSet))
modelviewsets = filter(lambda x: "bridger" not in x.__module__ and x not in get_all_subclasses(viewsets.InfiniteDataModelView), get_all_subclasses(viewsets.ModelViewSet))
inf_modelviewsets = filter(lambda x: "bridger" not in x.__module__, get_all_subclasses(viewsets.InfiniteDataModelView))

remote_models = get_specfics_module.send(sender = models)
if remote_models:
    _, models = remote_models[0]
remote_serializers = get_specfics_module.send(sender = serializers)
if remote_serializers:
    _, serializers = remote_serializers[0]
remote_representationviewsets = get_specfics_module.send(sender = representationviewsets)
if remote_representationviewsets:
    _, representationviewsets = remote_representationviewsets[0]
remote_modelviewsets = get_specfics_module.send(sender = modelviewsets)
if remote_modelviewsets:
    _, modelviewsets = remote_modelviewsets[0]
remote_inf_modelviewsets = get_specfics_module.send(sender = inf_modelviewsets)
if remote_inf_modelviewsets:
    _, inf_modelviewsets = remote_inf_modelviewsets[0]

if len([imvs for imvs in inf_modelviewsets]) == 0:
    inf_modelviewsets = [None]

@pytest.mark.django_db 
class TestProject:
    @pytest.mark.parametrize("model", models)
    def test_models(self, model):
        # print(mvs.__name__)
        # print(mvs.__module__)
        # print(model.__dict__)
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

    # @pytest.mark.parametrize("imvs", inf_modelviewsets)
    # def test_inf_modelviewsets(self, imvs, admin_client):
    #     if imvs:
    #         my_test = TestViewSetClass(imvs)
    #         my_test.execute_test(admin_client)