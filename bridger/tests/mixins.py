from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from django.contrib.auth import get_user_model
from rest_framework import status

from .utils import get_model_factory, format_number
import json
from termcolor import colored


class TestModelClass:
    def __init__(self, model):
        self.model = model
        self.factory = get_model_factory(model)

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
            country_queryset = self.model.objects.all()
            assert country_queryset.count() == 0
            for _ in range(100):
                self.factory()
            assert country_queryset.count() == 100
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
        self.factory = get_model_factory(rmvs().serializer_class.Meta.model)

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
            print("- TestViewSetClass:test_instancerepresentationviewset", colored("WARNING - factory not found for "+self.rmvs().serializer_class.Meta.model.__name__, 'yellow'))
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
        self.factory = get_model_factory(mvs().serializer_class.Meta.model)

    # ----- LIST ROUTE TEST ----- #
    #Test viewset "get": "list"
    def test_viewset(self):
        request = APIRequestFactory().get("")
        request.user = SuperUser.get_user()
        vs = self.mvs.as_view({"get": "list"})
        response = vs(request)
        assert response.status_code == status.HTTP_200_OK
        assert response.data
        print("\n- TestViewSetClass:test_viewset", colored("PASSED", 'green'))  
    
    #Test viewset "get": "list" -> aggregation
    def test_aggregation(self, namefield=None):
        request = APIRequestFactory().get("")
        request.user = SuperUser.get_user()
        vs = self.mvs.as_view({"get": "list"})
        response = vs(request)
        assert response.status_code == status.HTTP_200_OK
        if not response.data.get("aggregates"):
            print("- TestViewSetClass:test_aggregation:"+self.mvs.__name__, colored("WARNING - aggregates not found in "+self.mvs.__name__, 'yellow'))
        else:
            if namefield:
                assert response.data.get("aggregates").get(namefield)
                assert response.data.get("aggregates").get(namefield).get("#") == format_number(self.mvs().serializer_class.Meta.model.objects.count())
            print("- TestViewSetClass:test_aggregation", colored("PASSED", 'green')) 

    #Test viewset "post": "create"
    def test_postviewset(self):
        if self.factory is None:
            print("- TestViewSetClass:test_postviewset", colored("WARNING - factory not found for "+self.mvs().serializer_class.Meta.model.__name__, 'yellow'))
        else:
            request = APIRequestFactory().get("")
            serializer = self.mvs().serializer_class(self.factory(), context= {'request': Request(request)})
            request = APIRequestFactory().post("", serializer.data)
            request.user = SuperUser.get_user()
            vs = self.mvs.as_view({"post": "create"})
            response = vs(request)
            assert response.status_code == status.HTTP_201_CREATED
            assert response.data.get('instance')
            print("- TestViewSetClass:test_postviewset", colored("PASSED", 'green')) 

    #Test viewset "post": "create" with admin_client
    def test_postclientviewset(self, admin_client):
        if self.factory is None:
            print("- TestViewSetClass:test_postserializerviewset", colored("WARNING - factory not found for "+self.mvs().serializer_class.Meta.model.__name__, 'yellow'))
        else:
            request = APIRequestFactory().get("")
            vs = self.mvs()
            serializer = vs.serializer_class(self.factory(), context= {'request': Request(request)})
            response = admin_client.post(vs._get_endpoint(request),
                                json.dumps(serializer.data),
                                content_type='application/json')
            assert response.status_code == status.HTTP_201_CREATED
            assert response.json().get('instance')
            print("- TestViewSetClass:test_postserializerviewset", colored("PASSED", 'green'))  

    # TODO Test viewset "delete": "destroy_multiple"
    #def test_delete_allviewset(self):


    # ----- DETAIL ROUTE TEST ----- #
    # Test viewset "get": "retrieve"
    def test_instanceviewset(self):
        if self.factory is None:
            print("- TestViewSetClass:test_instanceviewset", colored("WARNING - factory not found for "+self.mvs().serializer_class.Meta.model.__name__, 'yellow'))
        else:
            request = APIRequestFactory().get("")
            request.user = SuperUser.get_user()
            vs = self.mvs.as_view({"get": "retrieve"})
            obj = self.factory()
            response = vs(request, pk=obj.pk)
            assert response.status_code == status.HTTP_200_OK
            assert response.data.get('instance')
            print("- TestViewSetClass:test_instanceviewset", colored("PASSED", 'green'))  
    
    # Test "delete": "destroy"
    def test_deleteviewset(self):
        if self.factory is None:
            print("- TestViewSetClass:test_deleteviewset", colored("WARNING - factory not found for "+self.mvs().serializer_class.Meta.model.__name__, 'yellow'))
        else:
            request = APIRequestFactory().delete("")
            request.user = SuperUser.get_user()
            vs = self.mvs.as_view({"delete": "destroy"})
            response = vs(request, pk=self.factory().pk)
            assert response.status_code == status.HTTP_204_NO_CONTENT
            print("- TestViewSetClass:test_deleteviewset", colored("PASSED", 'green'))  

    # Test "put": "update"
    def test_uptdateviewset(self):
        if self.factory is None:
            print("- TestViewSetClass:test_uptdateviewset", colored("WARNING - factory not found for "+self.mvs().serializer_class.Meta.model.__name__, 'yellow'))
        else:
            request = APIRequestFactory().get("")
            obj = self.factory()
            serializer = self.mvs().serializer_class(obj, context= {'request': Request(request)})
            request = APIRequestFactory().put("", serializer.data)
            request.user = SuperUser.get_user()
            
            vs = self.mvs.as_view({"put": "update"})
            response = vs(request, pk=obj.pk)
            assert response.status_code == status.HTTP_200_OK
            assert response.data.get('instance')
            print("- TestViewSetClass:test_uptdateviewset", colored("PASSED", 'green'))  

    #Test "patch": "partial_update",
    def test_patchviewset(self):
        if self.factory is None:
            print("- TestViewSetClass:test_patchviewset", colored("WARNING - factory not found for "+self.mvs().serializer_class.Meta.model.__name__, 'yellow'))
        else:
            request = APIRequestFactory().get("")
            obj = self.factory()
            serializer = self.mvs().serializer_class(obj, context= {'request': Request(request)})
            request = APIRequestFactory().patch("", serializer.data)
            request.user = SuperUser.get_user()
            
            vs = self.mvs.as_view({"patch": "partial_update"})
            response = vs(request, pk=obj.pk)
            assert response.status_code == status.HTTP_200_OK
            assert response.data.get('instance')
            print("- TestViewSetClass:test_patchviewset", colored("PASSED", 'green'))  


    # Test "get": "history_list" ??
    # Test "get": "history_retrieve" ??
    # 'get': 'highlight' ??

    # TODO relating to issue #20
    # def test_allviewset(self):
    #     request = APIRequestFactory().get("")
    #     request.user = SuperUser.get_user()
    #     vs = self.viewset( kwargs={})
    #     print(vs._get_endpoints(request))

    def execute_test(self, admin_client, aggregates=None):
        # ----- LIST ROUTE TEST ----- #
        self.test_viewset()
        self.test_aggregation(aggregates)
        self.test_postviewset()
        self.test_postclientviewset(admin_client)
        # ----- DETAIL ROUTE TEST ----- #
        self.test_instanceviewset()
        self.test_deleteviewset()
        self.test_uptdateviewset()
        self.test_patchviewset()
        #Test "get": "history_list"
        #Test "get": "history_retrieve"

        # self.test_allviewset()
