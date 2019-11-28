from django.urls import path
from .views import test_response

urlpatterns = [
    path("test/<int:pk>/", test_response, name="test"),
]
