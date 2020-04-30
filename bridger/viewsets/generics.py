from rest_framework.generics import GenericAPIView as OriginalGenericAPIView


class GenericAPIView(OriginalGenericAPIView):
    def get_serializer_changes(self, serializer):
        return serializer

    def get_serializer(self, *args, **kwargs):
        return self.get_serializer_changes(super().get_serializer(*args, **kwargs))
