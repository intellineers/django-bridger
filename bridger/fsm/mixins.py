import inspect
import logging
import pprint
from contextlib import suppress
from functools import partial, partialmethod
from optparse import OptionParser

from django.urls import resolve
from django_fsm import FSMField, TransitionNotAllowed, get_available_user_FIELD_transitions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse, NoReverseMatch
from rest_framework.serializers import SerializerMetaclass

from bridger.serializers import FSMStatusField, register_resource

logger = logging.getLogger(__name__)


# We have to move the method generation into a method, because we need a real new instance of this method everytime
def get_method(transition):
    def method(self, request: Request, transition=transition, pk=None, **kwargs) -> Response:
        return self.fsm_route(request, transition.name)

    return method


class FSMViewSetMixinMetaclass(type):
    """Metaclass for dynamically creating all FSM Routes"""

    def __new__(cls, name, bases, dct):
        _class = super().__new__(cls, name, bases, dct)

        # The class needs the field FSM_MODELFIELDS to know which transitions it needs to add
        if hasattr(_class, "get_model"):
            model = _class.get_model()

            if model:
                setattr(_class, "FSM_BUTTONS", getattr(_class, "FSM_BUTTONS", set()))
                # The model potentially has multiple FSMFields, which needs to be iterated over
                for field in filter(lambda f: isinstance(f, FSMField), model._meta.fields):
                    # Get all transitions, by calling the partialmethod defined by django-fsm
                    transitions = getattr(model, f"get_all_{field.name}_transitions")(model())

                    # Since the method above can potentially return a transition multiple times
                    # i.e. when a transitions has multiple sources, we need to filter out those transitions
                    _discovered_transitions = list()

                    for transition in transitions:
                        if transition.name in _discovered_transitions:
                            continue
                        else:
                            _discovered_transitions.append(transition.name)

                        # Get the Transition Button and add it to the front of the instance buttons
                        button = transition.custom.get("_transition_button")
                        _class.FSM_BUTTONS.add(button)

                        # Create a method that calls fsm_route with the request and the action name
                        method = get_method(transition)

                        # We need to manually change the method name, otherwise django-fsm won't
                        # Add this method to the URLs

                        # Wrap the above defined method in the action decorator
                        # IMPORTANT: This needs to happen after we changed the method name
                        # therefore we cannot use the proper decorator
                        method.__name__ = transition.name
                        method.__doc__ = transition.method.__doc__

                        wrapped_method = action(detail=True, methods=["GET", "PATCH"])(method)

                        # Set the method as a attribute of the class that implements this
                        # metaclass
                        setattr(_class, transition.name, wrapped_method)

        return _class


class FSMViewSetMixin(metaclass=FSMViewSetMixinMetaclass):
    def handle_exception(self, exc: Exception) -> Response:
        if isinstance(exc, TransitionNotAllowed):
            return Response({"non_field_errors": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)

    def fsm_route(self, request: Request, action: str) -> Response:
        obj = self.get_object()
        serializer_class = self.get_serializer_class()

        serializer_context = self.get_serializer_context()

        if request.method == "GET":
            return Response(serializer_class(instance=obj, context=serializer_context).data)

        serializer = serializer_class(instance=obj, data=request.data, partial=True, context=serializer_context)
        if serializer.is_valid():
            if len(serializer.validated_data) > 0:
                obj = serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        errors = None
        if hasattr(obj, f"can_{action}"):
            errors = getattr(obj, f"can_{action}")()

        if errors is None or len(errors.keys()) == 0:
            obj.fsm_context = {"current_user": request.user}
            getattr(obj, action)()
            obj.save()

            serializer = serializer_class(instance=obj, context=serializer_context)
            return Response(serializer.data)

        return Response(errors, status=status.HTTP_412_PRECONDITION_FAILED)


class FSMSerializerMetaclass(SerializerMetaclass):
    def __new__(cls, name, bases, dct):
        _class = super().__new__(cls, name, bases, dct)
        with suppress(AttributeError):
            model = _class.Meta.model
            for field in filter(lambda f: isinstance(f, FSMField), model._meta.fields):
                transitions = getattr(model, f"get_all_{field.name}_transitions")(model())
                for transition in transitions:

                    def method(self, instance, request, user, field, transition):
                        # if self.context["view"].historical_mode:
                        #     return {}

                        transitions = get_available_user_FIELD_transitions(instance, user, field)
                        if transition.name in [t.name for t in transitions]:
                            url = resolve(request.path_info)
                            namespace = f"{url.namespace}:" if url.namespace else ""
                            base_url_name = url.url_name.split("-")[:-1]

                            # We need to pass the kwargs from the view through to the reverse call
                            # And additionally pass in the instance.id as the pk
                            # NOTE: What happens if the reverse parameter is not called pk?
                            # NOTE: Is that even possible?

                            # If the view is not in the context, we just create an empty keyword dict.
                            # FIXME: This should actually never happen
                            try:
                                kwargs = self.context["view"].kwargs
                            except KeyError:
                                kwargs = {}
                            
                            kwargs.update({"pk": instance.id})
                            try:
                                endpoint = reverse(
                                    f"{namespace}{'-'.join(base_url_name)}-{transition.name}", kwargs=kwargs, request=request,
                                )
                            except NoReverseMatch:
                                return {}

                            return {transition.name: endpoint}
                        return {}

                    wrapped_method = register_resource()(partial(method, field=field, transition=transition))
                    wrapped_method.__name__ = transition.name

                    setattr(
                        _class, transition.name, wrapped_method,
                    )

        return _class
