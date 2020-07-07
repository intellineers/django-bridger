from django.apps import AppConfig


class Tests2Config(AppConfig):
    name = "tests2"

    def ready(self):
        from . import receivers
