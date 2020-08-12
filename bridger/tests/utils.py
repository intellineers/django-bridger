from django.apps import apps
import importlib 
import factory
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from django.urls import reverse
import json

from functools import partial
from typing import Any, Dict

from factory import Factory
from factory.base import StubObject

def get_all_subclasses(klass):
    for subclass in klass.__subclasses__():
        yield subclass
        yield from get_all_subclasses(subclass)
        
def get_model_factory(model):
    mf = [cls for cls in factory.django.DjangoModelFactory.__subclasses__() if cls._meta.model == model]
    if mf:
        return mf[0]
    return None

def get_data_factory_mvs(obj, mvs, delete=False):
    request = APIRequestFactory().get("")
    serializer = mvs().serializer_class(obj, context= {'request': Request(request)})

    fields_models = [m.name for m in mvs().serializer_class.Meta.model._meta.get_fields()]
    data = {}
    for key, value in serializer.data.items():
        if key in fields_models:
            data[key] = value
    # delete object for create with post method
    if delete:
        mvs().serializer_class.Meta.model.objects.filter(pk = obj.pk).delete()
    return data

def get_kwargs(obj, mvs, request):
    fields_models = [m for m in mvs().serializer_class.Meta.model._meta.get_fields()]         
    serializer = mvs().serializer_class(obj, context= {'request': request})
    kwargs={}
    for field in fields_models:
        if field.is_relation and field.name in serializer.data.keys():
            kwargs[field.name+"_id"] = serializer.data[field.name]
    return kwargs


def generate_dict_factory(factory: Factory):
    def convert_dict_from_stub(stub: StubObject) -> Dict[str, Any]:
        stub_dict = stub.__dict__
        for key, value in stub_dict.items():
            if isinstance(value, StubObject):
                stub_dict[key] = convert_dict_from_stub(value)
        return stub_dict

    def dict_factory(factory, **kwargs):
        stub = factory.stub(**kwargs)
        stub_dict = convert_dict_from_stub(stub)
        return stub_dict

    return partial(dict_factory, factory)

def format_number(number, is_pourcent=False, decimal=2):
    number = number if number else 0
    return f'{number:,.{decimal}{"%" if is_pourcent else "f"}}'