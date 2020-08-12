from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from django.contrib.auth import get_user_model
from rest_framework import status

from .utils import get_model_factory, format_number, get_data_factory_mvs, get_kwargs
from termcolor import colored
import json

class TestModelClass:
    def __init__(self, model):
        self.model = model
        self.factory = get_model_factory(model)
    
    def test_get_endpoint_basename(self):
        assert self.model.get_endpoint_basename()
        print("- TestModelClass:test_get_endpoint_basename", colored("PASSED", 'green'))

    def test_representation_endpoint(self):
        assert self.model.get_representation_endpoint()
        assert self.model.get_representation_endpoint() == self.model._meta.app_label+":"+self.model.__name__.lower()+"representation-list"
        print("- TestModelClass:test_representation_endpoint", colored("PASSED", 'green'))

    def test_representation_value_key(self):
        assert self.model.get_representation_value_key()
        assert self.model.get_representation_value_key() == "id"
        print("- TestModelClass:test_representation_value_key", colored("PASSED", 'green'))

    def test_representation_label_key(self):
        assert self.model.get_representation_label_key()
        print("- TestModelClass:test_representation_label_key", colored("PASSED", 'green'))

    def test_count_model(self):
        if self.factory is None:
            print("- TestModelClass:test_count_model", colored("WARNING - factory not found for "+self.model.__name__, 'yellow'))
        else:
            models = self.model.objects.all()
            assert models.count() == 0
            for _ in range(4):
                self.factory()
            assert models.count() == 4
            print("- TestModelClass:test_count_model", colored("PASSED", 'green')) 

    def test_str(self):
        if self.factory is None:
            print("- TestModelClass:test_str", colored("WARNING - factory not found for "+self.model.__name__, 'yellow'))
        else:
            obj = self.factory()
            assert str(obj)
            assert isinstance(str(obj), str)
            print("- TestModelClass:test_str", colored("PASSED", 'green'))

    def test_field(self):
        if self.factory is None:
            print("- TestModelClass:test_field", colored("WARNING - factory not found for "+self.model.__name__, 'yellow'))
        else:
            obj = self.factory()
            for field in obj._meta.get_fields():
                assert field
            print("- TestModelClass:test_field", colored("PASSED", 'green'))

    def execute_test(self):
        self.test_get_endpoint_basename()
        self.test_representation_endpoint()
        self.test_representation_value_key()
        self.test_representation_label_key()
        self.test_count_model()
        self.test_str()
        self.test_field()
    

class TestSerializerClass:
    def __init__(self, serializer):
        self.serializer = serializer
        self.factory = get_model_factory(serializer.Meta.model)
    
    def test_serializer(self):
        if self.factory is None:
            print("\n- TestSerializerClass:test_serializer:"+self.serializer.__name__, colored("WARNING - factory not found for "+self.serializer.Meta.model.__name__, 'yellow'))
        else:
            request = APIRequestFactory().get("")
            serializer = self.serializer(self.factory(), context= {'request': Request(request)})
            assert serializer.data
            print("\n- TestSerializerClass:test_serializer:"+self.serializer.__name__, colored("PASSED", 'green'))

    def execute_test(self):
        self.test_serializer()


class SuperUser:
    @classmethod
    def get_user(cls):
        try:
            superuser = get_user_model().objects.get(username="test_user")
        except (get_user_model().DoesNotExist, get_user_model().MultipleObjectsReturned):
            superuser = get_user_model().objects.create(username="test_user", password="ABC", is_active=True, is_superuser=True)
        return superuser


class TestrepresentationViewSetClass:
    def __init__(self, rmvs):
        self.rmvs = rmvs
        self.factory = get_model_factory(rmvs().get_serializer_class().Meta.model)

    # ----- LIST ROUTE TEST ----- #
    #Test representationviewset "get": "list"
    def test_representationviewset(self):
        request = APIRequestFactory().get("")
        request.user = SuperUser.get_user()
        vs = self.rmvs.as_view({"get": "list"})
        response = vs(request)
        assert response.status_code == status.HTTP_200_OK
        assert response.data
        print("\n- TestViewSetClass:test_representationviewset", colored("PASSED", 'green'))  

    
    # ----- DETAIL ROUTE TEST ----- #
    #Test representationviewset "get": "retrieve"
    def test_instancerepresentationviewset(self):
        if self.factory is None:
            print("- TestViewSetClass:test_instancerepresentationviewset", colored("WARNING - factory not found for "+self.rmvs().get_serializer_class().Meta.model.__name__, 'yellow'))
        else:
            request = APIRequestFactory().get("")
            request.user = SuperUser.get_user()
            vs = self.rmvs.as_view({"get": "retrieve"})
            obj = self.factory()
            response = vs(request, pk=obj.pk)
            assert response.status_code == status.HTTP_200_OK
            assert response.data.get('instance')
            print("- TestViewSetClass:test_instancerepresentationviewset", colored("PASSED", 'green')) 

    
    def execute_test(self, admin_client):
        # ----- LIST ROUTE TEST ----- #
        self.test_representationviewset()
        self.test_instancerepresentationviewset()
    

class TestViewSetClass:
    def __init__(self, mvs):
        self.mvs = mvs
        self.factory = get_model_factory(mvs().get_serializer_class().Meta.model)

    # test viewset Option request
    def test_option_request(self):
        if self.factory is None:
            print("- TestViewSetClass:test_option_request", colored("WARNING - factory not found for "+self.mvs().get_serializer_class().Meta.model.__name__, 'yellow'))
        else:
            request = APIRequestFactory().options("")
            request.user = SuperUser.get_user()      
            kwargs = get_kwargs(self.factory(), self.mvs, request)
            vs = self.mvs.as_view({"options": "options"})
            response = vs(request, **kwargs)
            assert response.status_code == status.HTTP_200_OK
            assert response.data.get("fields")
            assert response.data.get("identifier")
            assert response.data.get("pagination")
            # assert response.data.get("pk")
             # assert response.data.get("type")
            # assert response.data.get("filter_fields")
            # assert response.data.get("search_fields")
            # assert response.data.get("ordering_fields")
            assert response.data.get("buttons")
            assert response.data.get("display")
            assert response.data.get("titles")
            assert response.data.get("endpoints")
            # assert response.data.get("preview")
            print("\n- TestViewSetClass:test_option_request", colored("PASSED", 'green'))  


    # ----- LIST ROUTE TEST ----- #
    # Test viewset "get": "list"
    def test_viewset(self):
        if self.factory is None:
            print("- TestViewSetClass:test_viewset", colored("WARNING - factory not found for "+self.mvs().get_serializer_class().Meta.model.__name__, 'yellow'))
        else:
            request = APIRequestFactory().get("")
            request.user = SuperUser.get_user()      
            kwargs = get_kwargs(self.factory(), self.mvs, request)
            vs = self.mvs.as_view({"get": "list"})
            response = vs(request, **kwargs)
            assert response.status_code == status.HTTP_200_OK
            assert response.data
            assert response.data.get("results")
            print("- TestViewSetClass:test_viewset", colored("PASSED", 'green'))  

    # Test viewset "get": "list" -> aggregation
    def test_aggregation(self, namefield=None):
        if self.factory is None:
            print("- TestViewSetClass:test_aggregation", colored("WARNING - factory not found for "+self.mvs().get_serializer_class().Meta.model.__name__, 'yellow'))
        else:
            request = APIRequestFactory().get("")
            request.user = SuperUser.get_user()
            kwargs = get_kwargs(self.factory(), self.mvs, request)
            vs = self.mvs.as_view({"get": "list"})
            response = vs(request, **kwargs)
            assert response.status_code == status.HTTP_200_OK
            assert response.data.get("results")
            if not response.data.get("aggregates"):
                print("- TestViewSetClass:test_aggregation:"+self.mvs.__name__, colored("WARNING - aggregates not found in "+self.mvs.__name__, 'yellow'))
            else:
                if namefield:
                    assert response.data.get("aggregates").get(namefield)
                    assert response.data.get("aggregates").get(namefield).get("#") == format_number(self.mvs().get_serializer_class().Meta.model.objects.count())
                print("- TestViewSetClass:test_aggregation", colored("PASSED", 'green')) 

    # Test viewset "get": "list" with client and endpoint
    def test_get_client_endpointviewset(self, admin_client):
        if self.factory is None:
            print("- TestViewSetClass:test_get_client_endpointviewset", colored("WARNING - factory not found for "+self.mvs().get_serializer_class().Meta.model.__name__, 'yellow'))
        else:
            request = APIRequestFactory().get("")
            request.user = SuperUser.get_user()
            obj = self.factory()
            self.mvs.kwargs = get_kwargs(obj, self.mvs, request)
            ep = self.mvs.endpoint_config_class(self.mvs, request, instance=False)
            response = admin_client.get(ep.get_endpoint())
            assert response.status_code == status.HTTP_200_OK
            assert response.data.get("results")
            print("- TestViewSetClass:test_get_client_endpointviewset", colored("PASSED", 'green'))  

    # Test viewset "post": "create"
    def test_postviewset(self):
        if self.factory is None:
            print("- TestViewSetClass:test_postviewset", colored("WARNING - factory not found for "+self.mvs().get_serializer_class().Meta.model.__name__, 'yellow'))
        else:
            obj = self.factory()
            data = get_data_factory_mvs(obj, self.mvs, delete=True)
            request = APIRequestFactory().post("", data)
            request.user = SuperUser.get_user()
            kwargs = get_kwargs(obj, self.mvs, request)
            vs = self.mvs.as_view({"post": "create"})
            response = vs(request, **kwargs)
            assert response.status_code == status.HTTP_201_CREATED
            assert response.data.get('instance')
            print("- TestViewSetClass:test_postviewset", colored("PASSED", 'green')) 

    # Test viewset "post": "create" with client and endpoint
    def test_post_client_endpointviewset(self, admin_client):
        if self.factory is None:
            print("- TestViewSetClass:test_post_client_endpointviewset", colored("WARNING - factory not found for "+self.mvs().get_serializer_class().Meta.model.__name__, 'yellow'))
        else:
            obj = self.factory()
            data = get_data_factory_mvs(obj, self.mvs, delete=True)
            request = APIRequestFactory().post("", data)
            request.user = SuperUser.get_user()
            ep = self.mvs.endpoint_config_class(self.mvs, request, instance=False)
            response = admin_client.post(ep._get_create_endpoint(),
                                json.dumps(data),
                                content_type='application/json')
            assert response.status_code == status.HTTP_201_CREATED
            assert response.data.get('instance')
            print("- TestViewSetClass:test_post_client_endpointviewset", colored("PASSED", 'green'))  

    # TODO Test viewset "delete": "destroy_multiple"
    def test_destroy_multipleviewset(self):
        if self.factory is None:
            print("- TestViewSetClass:test_destroy_multipleviewset", colored("WARNING - factory not found for "+self.mvs().get_serializer_class().Meta.model.__name__, 'yellow'))
        else:
            request = APIRequestFactory().delete("")
            request.user = SuperUser.get_user()
            for _ in range(4):
                obj = self.factory()
            kwargs = get_kwargs(obj, self.mvs, request)
            vs = self.mvs.as_view({"delete": "destroy_multiple"})
            response = vs(request, **kwargs)
            assert response.status_code == status.HTTP_204_NO_CONTENT
            # assert not self.mvs().get_serializer_class().Meta.model.objects.filter(id=obj.id).exists()
        print("- TestViewSetClass:test_destroy_multipleviewset", colored("PASSED", 'green'))  
        
            
    # TODO Test viewset "delete": "destroy_multiple" with client and endpoint
    def test_destroy_multiple_client_endpointviewset(self, admin_client):
        if self.factory is None:
            print("- TestViewSetClass:test_destroy_multiple_client_endpointviewset", colored("WARNING - factory not found for "+self.mvs().get_serializer_class().Meta.model.__name__, 'yellow'))
        else:
            request = APIRequestFactory().delete("")
            request.user = SuperUser.get_user()
            list_id = []
            for _ in range(4):
                obj = self.factory()
                list_id.append(obj.id)
            request.data = list_id
            ep = self.mvs.endpoint_config_class(self.mvs, request, instance=False)
            response = admin_client.delete(ep._get_delete_endpoint())
            # queryset = self.mvs().get_serializer_class().Meta.model.objects.filter(id__in=data)
            # destroyed = queryset.delete()
            # print(destroyed)
            assert response.status_code == status.HTTP_204_NO_CONTENT


    # Test viewset "get_list_title"
    def test_get_list_title(self):
        if self.factory is None:
            print("- TestViewSetClass:test_get_list_title", colored("WARNING - factory not found for "+self.mvs().get_serializer_class().Meta.model.__name__, 'yellow'))
        else:
            obj = self.factory()
            request = APIRequestFactory().get("")
            request.user = SuperUser.get_user()
            kwargs = get_kwargs(obj, self.mvs, request)
            vs =  self.mvs(kwargs=kwargs)
            assert vs.title_config_class(vs, request, instance=False).get_list_title()
            print("- TestViewSetClass:test_get_list_title", colored("PASSED", 'green'))  

    # Test viewset "get_list_title"
    def test_get_instance_title(self):
        if self.factory is None:
            print("- TestViewSetClass:test_get_instance_title", colored("WARNING - factory not found for "+self.mvs().get_serializer_class().Meta.model.__name__, 'yellow'))
        else:
            obj = self.factory()
            request = APIRequestFactory().get("")
            request.user = SuperUser.get_user()
            kwargs = get_kwargs(obj, self.mvs, request)
            vs =  self.mvs(kwargs=kwargs)
            assert vs.title_config_class(vs, request, instance=False).get_instance_title()
            print("- TestViewSetClass:test_get_instance_title", colored("PASSED", 'green'))  

    # Test viewset "get_create_title"
    def test_get_create_title(self):
        if self.factory is None:
            print("- TestViewSetClass:test_get_create_title", colored("WARNING - factory not found for "+self.mvs().get_serializer_class().Meta.model.__name__, 'yellow'))
        else:
            obj = self.factory()
            request = APIRequestFactory().get("")
            request.user = SuperUser.get_user()
            kwargs = get_kwargs(obj, self.mvs, request)
            vs =  self.mvs(kwargs=kwargs)
            assert vs.title_config_class(vs, request, instance=False).get_create_title()
            print("- TestViewSetClass:test_get_create_title", colored("PASSED", 'green'))  

    #-------------- DETAIL ROUTE TEST ------------------#
    # Test viewset "get": "retrieve"
    def test_instanceviewset(self):
        if self.factory is None:
            print("- TestViewSetClass:test_instanceviewset", colored("WARNING - factory not found for "+self.mvs().get_serializer_class().Meta.model.__name__, 'yellow'))
        else:
            request = APIRequestFactory().get("")
            request.user = SuperUser.get_user()
            obj = self.factory()
            kwargs = get_kwargs(obj, self.mvs, request)
            vs = self.mvs.as_view({"get": "retrieve"})
            response = vs(request, **kwargs, pk=obj.pk)
            assert response.status_code == status.HTTP_200_OK
            assert response.data.get('instance')
            print("- TestViewSetClass:test_instanceviewset", colored("PASSED", 'green'))  
    
    # Test "delete": "destroy"
    def test_deleteviewset(self):
        if self.factory is None:
            print("- TestViewSetClass:test_deleteviewset", colored("WARNING - factory not found for "+self.mvs().get_serializer_class().Meta.model.__name__, 'yellow'))
        else:
            request = APIRequestFactory().delete("")
            request.user = SuperUser.get_user()
            obj = self.factory()
            kwargs = get_kwargs(obj, self.mvs, request)
            vs = self.mvs.as_view({"delete": "destroy"})
            response = vs(request, **kwargs, pk=obj.pk)
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert not self.mvs().get_serializer_class().Meta.model.objects.filter(id=obj.id).exists()
            print("- TestViewSetClass:test_deleteviewset", colored("PASSED", 'green'))  

    # Test "put": "update"
    def test_uptdateviewset(self):
        if self.factory is None:
            print("- TestViewSetClass:test_uptdateviewset", colored("WARNING - factory not found for "+self.mvs().get_serializer_class().Meta.model.__name__, 'yellow'))
        else:
            obj = self.factory()
            data = get_data_factory_mvs(obj, self.mvs)
            request = APIRequestFactory().put("", data)
            request.user = SuperUser.get_user()
            kwargs = get_kwargs(obj, self.mvs, request)
            vs = self.mvs.as_view({"put": "update"})
            response = vs(request, **kwargs, pk=obj.pk)
            assert response.status_code == status.HTTP_200_OK
            assert response.data.get('instance')
            print("- TestViewSetClass:test_uptdateviewset", colored("PASSED", 'green'))  


    #Test "patch": "partial_update",
    def test_patchviewset(self):
        if self.factory is None:
            print("- TestViewSetClass:test_patchviewset", colored("WARNING - factory not found for "+self.mvs().get_serializer_class().Meta.model.__name__, 'yellow'))
        else:
            obj = self.factory()
            data = get_data_factory_mvs(obj, self.mvs) 
            request = APIRequestFactory().patch("", data)
            request.user = SuperUser.get_user()
            kwargs = get_kwargs(obj, self.mvs, request)
            vs = self.mvs.as_view({"patch": "partial_update"})
            response = vs(request, **kwargs, pk=obj.pk, data=data)
            assert response.status_code == status.HTTP_200_OK
            assert response.data.get('instance')
            print("- TestViewSetClass:test_patchviewset", colored("PASSED", 'green'))  

    # TODO Test "get": "history_list" ??
    # TODO Test "get": "history_retrieve" ??
    # TODO 'get': 'highlight' ??

    def execute_test(self, admin_client, aggregates=None):
        self.test_option_request()
        # ----- LIST ROUTE TEST ----- #
        self.test_viewset()
        self.test_aggregation(aggregates)
        self.test_get_client_endpointviewset(admin_client)
        self.test_postviewset()
        self.test_post_client_endpointviewset(admin_client)
        self.test_destroy_multipleviewset()
        self.test_destroy_multiple_client_endpointviewset(admin_client)
        self.test_get_list_title()
        self.test_get_instance_title()
        self.test_get_create_title()
        # # ----- DETAIL ROUTE TEST ----- #
        self.test_instanceviewset()
        self.test_deleteviewset()
        self.test_uptdateviewset()
        self.test_patchviewset()
        #Test "get": "history_list"
        #Test "get": "history_retrieve"