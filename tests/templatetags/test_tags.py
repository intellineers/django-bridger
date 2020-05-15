from django import template

from tests.models import ModelTest

register = template.Library()


class ModelTestImageNode(template.Node):
    def __init__(self, model_test):
        self.instance = model_test

    def render(self, context):
        if self.instance.image_field:
            return f"<img src='{self.instance.image_field.url}' />"
        return ""


@register.tag
def model_test_image(parser, token):
    args = token.split_contents()
    return ModelTestImageNode(ModelTest.objects.get(id=args[1]))
