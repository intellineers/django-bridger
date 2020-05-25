from typing import Dict

from django.template import Context, Template
from django.utils.safestring import SafeString

from bridger.settings import bridger_settings


def load_registered_templatetags() -> str:
    """Assembles the templatetags that are registered to bridger in the django load format"""
    if templatetags := bridger_settings.MARKDOWN_TEMPLATE_TAGS or "":
        templatetags = f"{{% load {' '.join(templatetags)} %}}"

    return templatetags


def compile_template_for_templatetag(templatetag: str) -> Template:
    """Compiles a template with the registered templatetags to resolve a single templatetag"""
    return Template(load_registered_templatetags() + templatetag)


def render_template_for_templatetag(templatetag: str, **context: Dict) -> SafeString:
    """Renders a template for a single templatetag"""
    template = compile_template_for_templatetag(templatetag)
    return template.render(Context(context))
