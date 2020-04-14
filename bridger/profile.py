from typing import Dict

from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.reverse import reverse

from bridger.viewsets import ModelViewSet
from bridger.serializers import ModelSerializer


def default_profile(request: Request) -> Dict:
    """Returns two endpoints, one for the profile image and one for the profile widget"""

    return {
        "image": "https://image.freepik.com/free-vector/businessman-profile-cartoon_18591-58479.jpg",
        "endpoint": reverse(
            "bridger:user-detail", args=[request.user.id], request=request
        ),
    }


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email")


class UserViewSet(ModelViewSet):

    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
