from django.apps import apps
import importlib 
import factory
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from rest_framework.authtoken.models import Token
from django.urls import reverse
import json

from functools import partial
from typing import Any, Dict

from factory import Factory
from factory.base import StubObject

from django.db import models
from bridger.tests.signals import add_kwargs, add_data_factory

def get_all_subclasses(klass):
    for subclass in klass.__subclasses__():
        yield subclass
        yield from get_all_subclasses(subclass)

def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])

def get_model_factory(model):
    # mf = [cls for cls in factory.django.DjangoModelFactory.__subclasses__() if cls._meta.model == model]
    mfs = [cls for cls in all_subclasses(factory.django.DjangoModelFactory) if cls._meta.model == model]
    if is_empty(mfs):
        return None
    else:
        mf = [mf for mf in mfs if mf.__name__== model.__name__+"Factory"]  
        if not is_empty(mf):
            return mf[0]
        else:      
            return mfs[0]

def get_data_factory_mvs(obj, mvs, delete=False, update=False, superuser=None):
    request = APIRequestFactory().get("")
    if superuser:
        request.user = superuser
        request.parser_context = {"view": mvs}
        serializer = mvs().serializer_class(obj, context= {'request': request})
    else:
        serializer = mvs().serializer_class(obj, context= {'request': Request(request)})

    # fields_models = [m.name for m in mvs().serializer_class.Meta.model._meta.get_fields()]
    dict_fields_models = {}
    for m in mvs().serializer_class.Meta.model._meta.get_fields():
        dict_fields_models[m.name] = m

    data = {}
    for key, value in serializer.data.items():
        if key in dict_fields_models.keys() and key != "frontend_settings":
            if key == "auth_token":
                data[key], created = Token.objects.get_or_create(user=obj)
            elif dict_fields_models[key].get_internal_type() == "FileField" or dict_fields_models[key].get_internal_type() == "ImageField" or key == "content_type" :
                # data[key] = open(value.replace("http://testserver/",""), 'rb')
                pass
            elif dict_fields_models[key].get_internal_type() == "JSONField":
                pass
            else:
                data[key] = value
        
    if (delete and superuser) or (update and superuser):
        kwargs = {"superuser": superuser, "obj": obj}
        remote_data_factory = add_data_factory.send(mvs, **kwargs)
        if remote_data_factory :
            _, r_datakwarg = remote_data_factory[0]
            data.update(r_datakwarg)
            superuser = r_datakwarg["superuser"]

    # delete object for create with post method
    if delete:
        mvs().serializer_class.Meta.model.objects.filter(pk = obj.pk).delete()

    return data, superuser

def get_kwargs(obj, mvs, request, data=None):
    fields_models = [m for m in mvs().serializer_class.Meta.model._meta.get_fields()] 
    mvs.kwargs = {}
    request.parser_context = {"view": mvs}
    
    serializer = mvs().serializer_class(obj, context= {'request': request, "view": mvs})
    
    # serializer = mvs().get_serializer(obj)
    kwargs = {}
    for field in fields_models:
        if field.is_relation and field.name in serializer.data.keys():
            
            if is_empty(serializer.data[field.name]) and data:          
                kwargs[field.name+"_id"] = data[field.name]
            else:
                kwargs[field.name+"_id"] = serializer.data[field.name]
    # inject the profile for test the view ex.(InChargeCustomerModelViewSet) of crm
    if hasattr(request.user, 'profile'):
        kwargs["profile"] = request.user.profile
        kwargs["user"] = request.user
    if data:
        kwargs["data"] = data
    kwargs["obj_factory"] = obj
    remote_kwargs = add_kwargs.send(mvs, **kwargs)
    if remote_kwargs:
        _, r_kwarg = remote_kwargs[0]
        kwargs.update(r_kwarg)  
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

# check if an element of a list is present in the other
contains = lambda lst1, lst2: any( elt in lst1  for elt in lst2 )

def is_intermediate_table_m2m(model):
    if "_" in model.__qualname__ and not is_empty(model._meta.unique_together) :
        list_models = [elt.lower() for elt in model.__qualname__.split("_")]
        list_models_id = [elt.lower()+"_id" for elt in model.__qualname__.split("_")]
        if (contains(list_models, model._meta.unique_together[0]) and
            contains(list_models, model.__dict__.keys()) and
            contains(list_models_id, model.__dict__.keys()) ):
            return True
    return False

        # print(model.__dict__.keys())
        # print(model._meta.__dict__)
        # print(list_models)
        # print(model._meta.unique_together)
      

def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True

def get_factory_custom_user():
    list_models = [m for m in get_all_subclasses(models.Model) if m.__name__ == ('User') and not m.__module__.startswith(('bridger', 'django', 'rest_framework', 'dynamic_preferences', 'eventtools')) 
                and not m._meta.abstract and not is_intermediate_table_m2m(m)] 

    userfactory = [get_model_factory(modl) for modl in list(dict.fromkeys(list_models)) if get_model_factory(modl) is not None]
    if not is_empty(userfactory):
        return userfactory[0]
    return None

def format_number(number, is_pourcent=False, decimal=2):
    number = number if number else 0
    return f'{number:,.{decimal}{"%" if is_pourcent else "f"}}'