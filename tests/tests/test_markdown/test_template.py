import pytest
from django.template import Template
from django.test import override_settings

from bridger.markdown import template


@override_settings(BRIDGER_SETTINGS={"MARKDOWN_TEMPLATE_TAGS": []})
def test_load_registered_templatetags_no_tags():
    assert (
        template.load_registered_templatetags() == ""
    ), "When no template tags are registered this should return an empty string"


def test_load_registered_templatetags():
    assert (
        template.load_registered_templatetags() == "{% load test_tags %}"
    ), "When test_tags are registered, then the load string needs to return those tags as being loaded."


@pytest.mark.django_db
def test_compile_template_for_templatetag(model_test):
    assert isinstance(template.compile_template_for_templatetag(f"{{% model_test_text {model_test.id} %}}"), Template,)


@pytest.mark.django_db
def test_render_template_for_templatetag(model_test):
    assert template.render_template_for_templatetag(f"{{% model_test_text {model_test.id} %}}") == model_test.text_field
