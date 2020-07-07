from django.dispatch import Signal

add_instance_button = Signal(providing_args=["many"])
add_additional_resource = Signal(providing_args=["serializer", "instance", "request", "user"])
