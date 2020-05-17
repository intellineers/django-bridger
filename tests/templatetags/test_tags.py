from django import template

from tests.models import ModelTest

register = template.Library()


class ModelTestTextNode(template.Node):
    def __init__(self, model_test):
        self.instance = model_test

    def render(self, context):
        return self.instance.text_field or ""


@register.inclusion_tag("tests/template_tags/model_test_image.html", takes_context=True)
def model_test_image(context, model_test_id):
    model_test = ModelTest.objects.get(id=model_test_id)
    if model_test.image_field:
        return {"model_test": model_test}
    return {}


@register.tag
def model_test_text(parser, token):
    args = token.split_contents()
    return ModelTestTextNode(ModelTest.objects.get(id=args[1]))
