import markdown
from markdown.extensions.tables import TableExtension
from markdown_blockdiag import BlockdiagExtension
from rest_framework.response import Response

from bridger.settings import bridger_settings


def get_markdown_docs(docs):
    try:
        with open(docs, "r") as f:
            return Response(markdown.markdown(f.read(), extensions=bridger_settings.DEFAULT_MARKDOWN_EXTENSIONS,))
    except FileNotFoundError:
        return Response(markdown.markdown(docs, extensions=bridger_settings.DEFAULT_MARKDOWN_EXTENSIONS,))
    except AttributeError:
        return Response("No documentation available.")
