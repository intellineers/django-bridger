from termcolor import colored
from django.apps import apps
import importlib 
import factory

class Utils:
    @classmethod
    def get_all_subclasses(cls, klass):
        for subclass in klass.__subclasses__():
            yield subclass
            yield from cls.get_all_subclasses(subclass)
            
    @classmethod 
    def get_model_factory(cls, model):
        mf = [cls for cls in factory.django.DjangoModelFactory.__subclasses__() if cls._meta.model == model]
        if mf:
            return mf[0]
        return None

    @classmethod
    def format_number(cls, number, is_pourcent=False, decimal=2):
        number = number if number else 0
        return f'{number:,.{decimal}{"%" if is_pourcent else "f"}}'

   
    
    
