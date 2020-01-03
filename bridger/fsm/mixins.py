import inspect
import logging
import pprint
from contextlib import suppress
from functools import partialmethod, partial
from optparse import OptionParser

from django_fsm import (
    FSMField,
    TransitionNotAllowed,
    get_available_user_FIELD_transitions,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import SerializerMetaclass

from bridger.serializers import FSMStatusField
from bridger.serializers import register_resource
from django.urls import resolve

from rest_framework.reverse import reverse

logger = logging.getLogger(__name__)


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
                        # Get the Transition Button and add it to the front of the instance buttons
                        button = transition.custom.get("_transition_button")

                        setattr(
                            _class,
                            "CUSTOM_INSTANCE_BUTTONS",
                            [button] + (getattr(_class, "CUSTOM_INSTANCE_BUTTONS", [])),
                        )
                        setattr(
                            _class,
                            "CUSTOM_LIST_INSTANCE_BUTTONS",
                            [button]
                            + (getattr(_class, "CUSTOM_LIST_INSTANCE_BUTTONS", [])),
                        )

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
    def handle_exception(self, exc: Exception) -> Response:
        if isinstance(exc, TransitionNotAllowed):
            return Response(
                {"non_field_errors": str(exc)}, status=status.HTTP_400_BAD_REQUEST
            )
        return super.handle_exception(exc)

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


class FSMSerializerMetaclass(SerializerMetaclass):
    def __new__(cls, name, bases, dct):
        _class = super().__new__(cls, name, bases, dct)
        with suppress(AttributeError):
            model = _class.Meta.model
            for field in filter(lambda f: isinstance(f, FSMField), model._meta.fields):
                transitions = getattr(model, f"get_all_{field.name}_transitions")(
                    model()
                )
                for transition in transitions:

                    def method(self, instance, request, user, field, transition):
                        transitions = get_available_user_FIELD_transitions(
                            instance, user, field
                        )
                        if transition in transitions:
                            url = resolve(request.path_info)
                            namespace = f"{url.namespace}:" if url.namespace else ""
                            base_url_name = url.url_name.split("-")[:-1]

                            endpoint = reverse(
                                f"{namespace}{'-'.join(base_url_name)}-{transition.name}",
                                args=[instance.id],
                                request=request,
                            )
                            return {transition.name: endpoint}
                        return {}

                    wrapped_method = register_resource()(
                        partial(method, field=field, transition=transition)
                    )
                    wrapped_method.__name__ = transition.name

                    setattr(
                        _class, transition.name, wrapped_method,
                    )

        return _class