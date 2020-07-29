from django.apps import apps
import importlib 
import factory


def get_all_subclasses(klass):
    for subclass in klass.__subclasses__():
        yield subclass
        yield from get_all_subclasses(subclass)
        
def get_model_factory(model):
    mf = [cls for cls in factory.django.DjangoModelFactory.__subclasses__() if cls._meta.model == model]
    if mf:
        return mf[0]
    return None

def format_number(number, is_pourcent=False, decimal=2):
    number = number if number else 0
    return f'{number:,.{decimal}{"%" if is_pourcent else "f"}}'

   
    
    
