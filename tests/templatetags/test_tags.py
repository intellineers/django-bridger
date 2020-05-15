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


class ModelTestTextNode(template.Node):
    def __init__(self, model_test):
        self.instance = model_test

    def render(self, context):
        return self.instance.text_field or ""


@register.tag
def model_test_image(parser, token):
    args = token.split_contents()
    return ModelTestImageNode(ModelTest.objects.get(id=args[1]))


@register.tag
def model_test_text(parser, token):
    args = token.split_contents()
    return ModelTestTextNode(ModelTest.objects.get(id=args[1]))
