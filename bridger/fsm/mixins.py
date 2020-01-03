import logging, pprint
from functools import partialmethod
from rest_framework.decorators import action
import inspect
from rest_framework.request import Request
from rest_framework.response import Response
from django_fsm import FSMField

logger = logging.getLogger(__name__)
from optparse import OptionParser


class FSMViewSetMixinMetaclass(type):
    """Metaclass for dynamically creating all FSM Routes"""

    def __new__(cls, name, bases, dct):
        _class = super().__new__(cls, name, bases, dct)

        # The class needs the field FSM_MODELFIELDS to know which transitions it needs to add
        if hasattr(_class, "get_model"):
            model = _class.get_model()
            if model:
                # The model potentially has multiple FSMFields, which needs to be iterated over
                for field in filter(
                    lambda f: isinstance(f, FSMField), model._meta.fields
                ):
                    # Get all transitions, by calling the partialmethod defined by django-fsm
                    transitions = getattr(model, f"get_all_{field.name}_transitions")(
                        model()
                    )
                    for transition in transitions:

                        # Create a method that calls fsm_route with the request and the action name
                        def method(self, request: Request, pk: int = None) -> Response:
                            return self.fsm_route(request, transition.name)

                        # We need to manually change the method name, otherwise django-fsm won't
                        # Add this method to the URLs
                        method.__name__ = transition.name

                        # Wrap the above defined method in the action decorator
                        # IMPORTANT: This needs to happen after we changed the method name
                        # therefore we cannot use the proper decorator
                        wrapped_method = action(detail=True, methods=["GET", "PATCH"])(
                            method
                        )

                        # Set the method as a attribute of the class that implements this
                        # metaclass
                        setattr(_class, transition.name, wrapped_method)

        return _class


class FSMViewSetMixin(metaclass=FSMViewSetMixinMetaclass):
    def fsm_route(self, request: Request, action: str) -> Response:
        obj = self.get_object()
        serializer_class = self.get_serializer_class()

        if request.method == "GET":
            return Response(
                serializer_class(instance=obj, context={"request": request}).data
            )

        serializer = serializer_class(
            instance=obj, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            if len(serializer.validated_data) > 0:
                obj = serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        errors = None
        if hasattr(obj, f"can_{action}"):
            errors = getattr(obj, f"can_{action}")()

        if errors is None or len(errors.keys()) == 0:
            getattr(obj, action)()
            obj.save()

            serializer = serializer_class(instance=obj, context={"request": request})
            return Response(serializer.data)

        return Response(errors, status=status.HTTP_412_PRECONDITION_FAILED)
