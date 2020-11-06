from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from django.contrib.auth import get_user_model
from rest_framework import status

from .utils import get_model_factory, format_number, get_data_factory_mvs, get_kwargs, generate_dict_factory, get_factory_custom_user
from termcolor import colored
import json
import factory
from django.db.models import Q
from bridger.tests.signals import add_factory, create_permission_allowed, delete_permission_allowed, update_permission_allowed, retrieve_permission_allowed, get_retrieve_id_obj

class TestModelClass:
    def __init__(self, model):
        self.model = model
        self.factory = get_model_factory(model)

    def test_get_endpoint_basename(self):
        if not hasattr(self.model, "get_endpoint_basename"):
            print("\n- TestModelClass:test_get_endpoint_basename:"+self.model.__name__, colored("WARNING - "+self.model.__name__+" has no attribute 'get_endpoint_basename'", 'yellow'))
        else:
            assert self.model.get_endpoint_basename()
            print("\n- TestModelClass:test_get_endpoint_basename", colored("PASSED", 'green'))


    def test_representation_endpoint(self):
        if not hasattr(self.model, "get_representation_endpoint"):
            print("- TestModelClass:test_representation_endpoint:"+self.model.__name__, colored("WARNING - "+self.model.__name__+" has no attribute 'get_representation_endpoint'", 'yellow'))
        else:
            assert self.model.get_representation_endpoint()
            if self.model.__name__ in ["BridgerPermission", "BridgerGroup"]:
                assert self.model.get_representation_endpoint() == self.model._meta.app_label+":grouprepresentation-list" or \
                self.model.get_representation_endpoint() == "grouprepresentation-list" 
            else:
                assert self.model.get_representation_endpoint() == self.model._meta.app_label+":"+self.model.__name__.lower()+"representation-list" or \
                self.model.get_representation_endpoint() == self.model.__name__.lower()+"representation-list"
            print("- TestModelClass:test_representation_endpoint", colored("PASSED", 'green'))

    def test_representation_value_key(self):
        if not hasattr(self.model, "get_representation_value_key"):
            print("- TestModelClass:test_representation_value_key:"+self.model.__name__, colored("WARNING - "+self.model.__name__+" has no attribute 'get_representation_value_key'", 'yellow'))
        else:
            assert self.model.get_representation_value_key()
            assert self.model.get_representation_value_key() == "id"
            print("- TestModelClass:test_representation_value_key", colored("PASSED", 'green'))

    def test_representation_label_key(self):
        if not hasattr(self.model, "get_representation_label_key"):
            print("- TestModelClass:test_representation_label_key:"+self.model.__name__, colored("WARNING - "+self.model.__name__+" has no attribute 'get_representation_label_key'", 'yellow'))
        else:
            assert self.model.get_representation_label_key()
            print("- TestModelClass:test_representation_label_key", colored("PASSED", 'green'))

    def test_count_model(self):
        if self.factory is None:
            print("- TestModelClass:test_count_model", colored("WARNING - factory not found for "+self.model.__name__, 'yellow'))
        else:
            if self.model.__name__ == "Activity" and "preceded_by" in self.model.__dict__:
                models = self.model.objects.filter(~Q(preceded_by=None))
            elif self.model.__name__ == "ActivityOccurrence" and "event" in self.model.__dict__:
                models = self.model.objects.filter(Q(event__preceded_by=None))
            elif self.model.__name__ == "BookingEntry" and "main_booking_entry" in self.model.__dict__:
                models = self.model.objects.filter(~Q(main_booking_entry=None))
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


class SuperUser:
    @classmethod
    def get_user(cls):
        userfactory = get_factory_custom_user()
        if userfactory:
            superuser = userfactory(is_active=True, is_superuser=True)
        else:
            try:
                superuser = get_user_model().objects.get(username="test_user")
            except (get_user_model().DoesNotExist, get_user_model().MultipleObjectsReturned):
                superuser = get_user_model().objects.create(username="test_user", password="ABC", is_active=True, is_superuser=True)
        return superuser


class TestSerializerClass:
    def __init__(self, serializer):
        self.serializer = serializer
        self.factory = get_model_factory(serializer.Meta.model)
    
    def test_serializer(self):
        if self.factory is None:
            print("\n- TestSerializerClass:test_serializer:"+self.serializer.__name__, colored("WARNING - factory not found for "+self.serializer.Meta.model.__name__, 'yellow'))
        else:
            request = APIRequestFactory().get("")
            request.user = SuperUser.get_user()
            request.parser_context = {}
            # serializer = self.serializer(self.factory(), context= {'request': Request(request)})
            serializer = self.serializer(self.factory(), context= {'request': request})
            assert serializer.data
            print("\n- TestSerializerClass:test_serializer:"+self.serializer.__name__, colored("PASSED", 'green'))

    def execute_test(self):
        self.test_serializer()



class TestrepresentationViewSetClass:
    def __init__(self, rmvs):
        self.rmvs = rmvs
        remote_factories = add_factory.send(self.rmvs)
        if remote_factories:
            _, self.factory = remote_factories[0]
        else:
            self.factory = get_model_factory(self.rmvs().get_serializer_class().Meta.model)

    # ----- LIST ROUTE TEST ----- #
    #Test representationviewset "get": "list"
    def test_representationviewset(self):
        if self.factory is None:
            print("- TestViewSetClass:test_representationviewset", colored("WARNING - factory not found for "+self.rmvs().get_serializer_class().Meta.model.__name__, 'yellow'))
        else:
            request = APIRequestFactory().get("")
            request.user = SuperUser.get_user()
            obj = self.factory()
            kwargs = get_kwargs(obj, self.rmvs, request)
            vs = self.rmvs.as_view({"get": "list"})
            response = vs(request, **kwargs)
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
            obj = self.factory()
            kwargs = get_kwargs(obj, self.rmvs, request)
            vs = self.rmvs.as_view({"get": "retrieve"})
            remote_retrieve_id_obj = get_retrieve_id_obj.send(self.rmvs, **kwargs)
            if remote_retrieve_id_obj:
                _, obj_pk = remote_retrieve_id_obj[0]
            else:
                obj_pk = obj.pk
            response = vs(request, **kwargs, pk=obj_pk)
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

        remote_factories = add_factory.send(self.mvs)
        if remote_factories:
            _, self.factory = remote_factories[0]
        else:
            self.factory = get_model_factory(self.mvs().get_serializer_class().Meta.model)

        remote_create_permission = create_permission_allowed.send(self.mvs) 
        if remote_create_permission:
            _, self.create_permission_allowed = remote_create_permission[0]
        else:
            self.create_permission_allowed = True

        remote_delete_permission = delete_permission_allowed.send(self.mvs) 
        if remote_delete_permission:
            _, self.delete_permission_allowed = remote_delete_permission[0]
        else:
            self.delete_permission_allowed = True

        remote_update_permission = update_permission_allowed.send(self.mvs) 
        if remote_update_permission:
            _, self.update_permission_allowed = remote_update_permission[0]
        else:
            self.update_permission_allowed = True

        remote_retrieve_permission = retrieve_permission_allowed.send(self.mvs) 
        if remote_retrieve_permission:
            _, self.retrieve_permission_allowed = remote_retrieve_permission[0]
        else:
            self.retrieve_permission_allowed = True
            
    # test viewset Option request
    def test_option_request(self, is_instance=False):
        if self.factory is None:
            print("\n- TestViewSetClass:test_option_request", colored("WARNING - factory not found for "+self.mvs().get_serializer_class().Meta.model.__name__, 'yellow'))
        else:     
            request = APIRequestFactory().options("")
            request.user = SuperUser.get_user()      

            if self.factory._meta.model.__name__ == "User":
                obj = request.user
            else:
                obj = self.factory()
            kwargs = get_kwargs(obj, self.mvs, request)
     
            remote_retrieve_id_obj = get_retrieve_id_obj.send(self.mvs, **kwargs)
            if remote_retrieve_id_obj:
                _, obj_pk = remote_retrieve_id_obj[0]
            else:
                obj_pk = obj.pk

            if is_instance and self.retrieve_permission_allowed:
                kwargs["pk"] = obj_pk
            vs = self.mvs.as_view({"options": "options"})
            response = vs(request, **kwargs)
            assert response.status_code == status.HTTP_200_OK
            if "buttons" in response.data.keys():
                if "custom_instance" in response.data.get("buttons").keys():
                    assert list(response.data["buttons"]["custom_instance"]) or len(list(response.data["buttons"]["custom_instance"])) == 0
            assert response.data.get("fields")
            assert response.data.get("identifier")
            # assert response.data.get("pagination")
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
            obj = self.factory()    
            kwargs = get_kwargs(obj, self.mvs, request)
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
            assert response.data
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
            if ep.get_endpoint():
                response = admin_client.get(ep.get_endpoint())
            else:
                response = admin_client.get(ep.get_list_endpoint())
            assert response.status_code == status.HTTP_200_OK
            assert response.data
            print("- TestViewSetClass:test_get_client_endpointviewset", colored("PASSED", 'green'))  

    # Test viewset "post": "create"
    def test_postviewset(self):
        if self.factory is None:
            print("- TestViewSetClass:test_postviewset", colored("WARNING - factory not found for "+self.mvs().get_serializer_class().Meta.model.__name__, 'yellow'))
        else:
            obj = self.factory()
            superuser = SuperUser.get_user()
            data, superuser = get_data_factory_mvs(obj, self.mvs, delete=True, superuser=superuser)
            request = APIRequestFactory().post("", data)
            request.user = superuser
            kwargs = get_kwargs(obj, self.mvs, request=request, data=data)
            vs = self.mvs.as_view({"post": "create"})
            response = vs(request, **kwargs)     
            if self.create_permission_allowed:
                assert response.status_code == status.HTTP_201_CREATED
                assert response.data.get('instance')
            else:
                assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
            print("- TestViewSetClass:test_postviewset", colored("PASSED", 'green')) 

    # Test viewset "post": "create" with client and endpoint
    def test_post_client_endpointviewset(self, admin_client):
        if self.factory is None:
            print("- TestViewSetClass:test_post_client_endpointviewset", colored("WARNING - factory not found for "+self.mvs().get_serializer_class().Meta.model.__name__, 'yellow'))
        else:
            obj = self.factory()
            superuser = SuperUser.get_user()
            data, superuser = get_data_factory_mvs(obj, self.mvs, delete=True, superuser=superuser)
            request = APIRequestFactory().post("", data)
            request.user = superuser
            self.mvs.kwargs = get_kwargs(obj, self.mvs, request, data=data)
            ep = self.mvs.endpoint_config_class(self.mvs, request=request, instance=False)
            if not self.create_permission_allowed:
                assert ep._get_create_endpoint() == None
            else:
                assert ep._get_create_endpoint()
                response = admin_client.post(ep._get_create_endpoint(),
                                data)
                assert response.status_code == status.HTTP_201_CREATED
                assert response.data.get('instance')
            print("- TestViewSetClass:test_post_client_endpointviewset", colored("PASSED", 'green'))  

    # Test viewset "delete": "destroy_multiple"
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
            if self.delete_permission_allowed:
                assert response.status_code == status.HTTP_204_NO_CONTENT
                # assert not self.mvs().get_serializer_class().Meta.model.objects.filter(id=obj.id).exists()
            else:
                assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
            
            print("- TestViewSetClass:test_destroy_multipleviewset", colored("PASSED", 'green'))  
        
            
    # Test viewset "delete": "destroy_multiple" with client and endpoint
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
            self.mvs.kwargs = get_kwargs(obj, self.mvs, request)
            ep = self.mvs.endpoint_config_class(self.mvs, request, instance=False)
            if not self.delete_permission_allowed:
                assert ep._get_delete_endpoint() == None
            else:
                assert ep._get_delete_endpoint()
                response = admin_client.delete(ep._get_delete_endpoint())
                # queryset = self.mvs().get_serializer_class().Meta.model.objects.filter(id__in=data)
                # destroyed = queryset.delete()
                # print(destroyed)
                assert response.status_code == status.HTTP_204_NO_CONTENT
            print("- TestViewSetClass:test_destroy_multiple_client_endpointviewset", colored("PASSED", 'green'))


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

    # Test viewset "test_get_instance_title"
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
            if self.factory._meta.model.__name__ == "User":
                obj = request.user
            else:
                obj = self.factory()
            kwargs = get_kwargs(obj, self.mvs, request)
            remote_retrieve_id_obj = get_retrieve_id_obj.send(self.mvs, **kwargs)
            if remote_retrieve_id_obj:
                _, obj_pk = remote_retrieve_id_obj[0]
            else:
                obj_pk = obj.pk
            vs = self.mvs.as_view({"get": "retrieve"})
            response = vs(request, **kwargs, pk=obj_pk)
            self.mvs.kwargs = kwargs
            if self.retrieve_permission_allowed :
                assert response.status_code == status.HTTP_200_OK
                assert response.data.get('instance')
            else:
                assert response.status_code == status.HTTP_404_NOT_FOUND
            print("- TestViewSetClass:test_instanceviewset", colored("PASSED", 'green'))  
    
    # Test "delete": "destroy"
    def test_deleteviewset(self):
        if self.factory is None:
            print("- TestViewSetClass:test_deleteviewset", colored("WARNING - factory not found for "+self.mvs().get_serializer_class().Meta.model.__name__, 'yellow'))
        else:
            request = APIRequestFactory().delete("")
            request.user = SuperUser.get_user()
            if self.factory._meta.model.__name__ == "User":
                obj = request.user
            else:
                obj = self.factory()
            kwargs = get_kwargs(obj, self.mvs, request)
            remote_retrieve_id_obj = get_retrieve_id_obj.send(self.mvs, **kwargs)
            if remote_retrieve_id_obj:
                _, obj_pk = remote_retrieve_id_obj[0]
            else:
                obj_pk = obj.pk
            vs = self.mvs.as_view({"delete": "destroy"})
            response = vs(request, **kwargs, pk=obj_pk)
            if self.delete_permission_allowed:
                assert response.status_code == status.HTTP_204_NO_CONTENT
                assert not self.mvs().get_serializer_class().Meta.model.objects.filter(id=obj_pk).exists()
            else:
                assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
            print("- TestViewSetClass:test_deleteviewset", colored("PASSED", 'green'))  

    # Test "put": "update"
    def test_uptdateviewset(self):
        if self.factory is None:
            print("- TestViewSetClass:test_uptdateviewset", colored("WARNING - factory not found for "+self.mvs().get_serializer_class().Meta.model.__name__, 'yellow'))
        else:
            obj = self.factory()
            superuser = SuperUser.get_user()
            data, superuser = get_data_factory_mvs(obj, self.mvs, update=True, superuser=superuser) 
            request = APIRequestFactory().put("", data)
            request.user = superuser
            kwargs = get_kwargs(obj, self.mvs, request)   
            remote_retrieve_id_obj = get_retrieve_id_obj.send(self.mvs, **kwargs)
            if remote_retrieve_id_obj:
                _, obj_pk = remote_retrieve_id_obj[0]
            else:
                obj_pk = obj.pk     
            vs = self.mvs.as_view({"put": "update"})
            response = vs(request, **kwargs, pk=obj_pk)   
            if self.update_permission_allowed:
                assert response.status_code == status.HTTP_200_OK
                assert response.data.get('instance')
            else:
                assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
            print("- TestViewSetClass:test_uptdateviewset", colored("PASSED", 'green'))  


    #Test "patch": "partial_update",
    def test_patchviewset(self):
        if self.factory is None:
            print("- TestViewSetClass:test_patchviewset", colored("WARNING - factory not found for "+self.mvs().get_serializer_class().Meta.model.__name__, 'yellow'))
        else:
            obj = self.factory()
            superuser = SuperUser.get_user()
            data, superuser = get_data_factory_mvs(obj, self.mvs, update=True, superuser=superuser)
            request = APIRequestFactory().patch("", data)
            request.user = superuser
            kwargs = get_kwargs(obj, self.mvs, request)
            remote_retrieve_id_obj = get_retrieve_id_obj.send(self.mvs, **kwargs)
            if remote_retrieve_id_obj:
                _, obj_pk = remote_retrieve_id_obj[0]
            else:
                obj_pk = obj.pk
            vs = self.mvs.as_view({"patch": "partial_update"})
            response = vs(request, **kwargs, pk=obj_pk, data=data)
            if self.update_permission_allowed:
                assert response.status_code == status.HTTP_200_OK
                assert response.data.get('instance')
            else:
                assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
            print("- TestViewSetClass:test_patchviewset", colored("PASSED", 'green'))  

    # TODO Test "get": "history_list" ??
    # TODO Test "get": "history_retrieve" ??
    # TODO 'get': 'highlight' ??

    def execute_test(self, admin_client, aggregates=None):
        self.test_option_request(is_instance=True)
        self.test_option_request()
        # ----- LIST ROUTE TEST ----- #
        self.test_viewset()
        self.test_aggregation(aggregates)
        self.test_get_client_endpointviewset(admin_client)
        self.test_postviewset()
        self.test_post_client_endpointviewset(admin_client)
        self.test_destroy_multipleviewset()
        self.test_destroy_multiple_client_endpointviewset(admin_client)
        # self.test_get_list_title()
        # self.test_get_instance_title()
        # self.test_get_create_title()
        # ----- DETAIL ROUTE TEST ----- #
        self.test_instanceviewset()
        self.test_deleteviewset()
        self.test_uptdateviewset()
        self.test_patchviewset()
        # Test "get": "history_list"
        # Test "get": "history_retrieve"


class TestInfViewSetClass(TestViewSetClass):

    def execute_test(self, admin_client, aggregates=None):
        self.test_option_request()
        self.test_viewset()