import django.dispatch

add_instance_button = django.dispatch.Signal(providing_args=[])
add_additional_resource = django.dispatch.Signal(providing_args=[])

