from typing import Dict

from django.template import Context, Template
from django.utils.safestring import SafeString
from markdown import markdown

from bridger.settings import bridger_settings


def load_registered_templatetags() -> str:
    """Assembles the templatetags that are registered to bridger in the django load format"""
    if templatetags := bridger_settings.MARKDOWN_TEMPLATE_TAGS or "":
        templatetags = f"{{% load {' '.join(templatetags)} %}}"

    return templatetags


def compile_template_for_templatetag(templatetag: str) -> Template:
    """Compiles a template with the registered templatetags to resolve a single templatetag"""
    return Template(load_registered_templatetags() + templatetag)


def render_template_for_templatetag(templatetag: str, **context) -> SafeString:
    """Renders a template for a single templatetag"""
    template = compile_template_for_templatetag(templatetag)
    return template.render(Context(context))


def resolve_templatetags(content: str, **context) -> str:
    """Resolves all templatetags of some content"""
    return Template(load_registered_templatetags() + content).render(Context(context))


def resolve_markdown(content: str, extensions=None) -> str:
    """Resolves the markdown of some content"""
    return markdown(content, extensions=extensions)


def resolve_content(content: str, extensions=None, **context) -> str:
    """Resolves the content by first resolving the templatetags and then resolving any potential markdown fields"""
    return resolve_markdown(resolve_templatetags(content, **context), extensions=extensions)
