# import pytest
# from rest_framework.test import APIRequestFactory

# from bridger.enums import Button, WidgetType
# from bridger.serializers import ModelSerializer
# from bridger.viewsets import ModelViewSet
# from tests.models import ModelTest


# class TestMetadataMixin:
#     def setup_method(self):
#         self.factory = APIRequestFactory()
#         self.request = self.factory.get("")

#     def test_widget_type_overwritten(self):
#         class MVS(ModelViewSet):
#             WIDGET_TYPE = "ABC"

#         assert MVS().get_widget_type(request=self.request) == "ABC"

#     def test_widget_type_default_list(self):
#         class MVS(ModelViewSet):
#             pass

#         assert (
#             MVS(kwargs={}).get_widget_type(request=self.request)
#             == WidgetType.LIST.value
#         )

#     def test_widget_type_default_instance(self):
#         class MVS(ModelViewSet):
#             pass

#         assert (
#             MVS(kwargs={"pk": 1}).get_widget_type(request=self.request)
#             == WidgetType.INSTANCE.value
#         )

#     def test_identifier_fail(self):
#         class MVS(ModelViewSet):
#             pass

#         with pytest.raises(AssertionError):
#             MVS().get_identifier(request=self.request)

#     def test_identifier_overwritten(self):
#         class MVS(ModelViewSet):
#             IDENTIFIER = "abc:abc"

#         assert MVS().get_identifier(request=self.request) == "abc:abc"

#     def test_identifier_from_content_type(self):
#         class MS(ModelSerializer):
#             class Meta:
#                 model = ModelTest
#                 fields = "__all__"

#         class MVS(ModelViewSet):
#             serializer_class = MS

#         assert MVS().get_identifier(request=self.request) == "tests:modeltest"

#     def test_get_endpoint_none(self):
#         class MVS(ModelViewSet):
#             pass

#         assert MVS().get_endpoint(request=self.request) is None

#     def test_get_endpoint(self):
#         class MVS(ModelViewSet):
#             ENDPOINT = "modeltest-list"

#         assert MVS().get_endpoint(request=self.request) is not None

#     @pytest.mark.parametrize(
#         "method",
#         [
#             "get_list_endpoint",
#             "get_instance_endpoint",
#             "get_create_endpoint",
#             "get_delete_endpoint",
#         ],
#     )
#     def test_get_x_endpoint_none_and_no_endpoint(self, method):
#         class MVS(ModelViewSet):
#             pass

#         assert getattr(MVS(), method)(request=self.request) is None

#     @pytest.mark.parametrize(
#         "method",
#         [
#             "get_list_endpoint",
#             "get_instance_endpoint",
#             "get_create_endpoint",
#             "get_delete_endpoint",
#         ],
#     )
#     def test_get_x_endpoint_none_but_endpoint(self, method):
#         class MVS(ModelViewSet):
#             ENDPOINT = "modeltest-list"

#         assert getattr(MVS(), method)(request=self.request) is not None

#     @pytest.mark.parametrize(
#         "attribute, method",
#         [
#             ("LIST_ENDPOINT", "get_list_endpoint"),
#             ("INSTANCE_ENDPOINT", "get_instance_endpoint"),
#             ("CREATE_ENDPOINT", "get_create_endpoint"),
#             ("DELETE_ENDPOINT", "get_delete_endpoint"),
#         ],
#     )
#     def test_get_list_endpoint(self, attribute, method):
#         class MVS(ModelViewSet):
#             pass

#         setattr(MVS, attribute, "modeltest-list")
#         assert getattr(MVS(), method)(request=self.request) is not None

#     def test_get_endpoints(self):
#         class MVS(ModelViewSet):
#             ENDPOINT = "modeltest-list"

#         assert set(MVS().get_endpoints(request=self.request, buttons=[]).keys()) == set(
#             ["list", "create", "instance", "delete"]
#         )

#     def test_get_endpoints_no_create_endpoint(self):
#         class MVS(ModelViewSet):
#             LIST_ENDPOINT = "modeltest-list"
#             INSTANCE_ENDPOINT = "modeltest-list"

#         buttons = [Button.NEW.value]
#         assert set(
#             MVS().get_endpoints(request=self.request, buttons=buttons).keys()
#         ) == set(["list", "instance"])
#         assert len(buttons) == 0

#     def test_get_endpoints_no_delete_endpoint(self):
#         class MVS(ModelViewSet):
#             LIST_ENDPOINT = "modeltest-list"
#             INSTANCE_ENDPOINT = "modeltest-list"

#         buttons = [Button.DELETE.value]
#         assert set(
#             MVS().get_endpoints(request=self.request, buttons=buttons).keys()
#         ) == set(["list", "instance"])
#         assert len(buttons) == 0
