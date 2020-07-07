from blockdiag.parser import ParseException
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.template import Context, Template, exceptions
from markdown_blockdiag.utils import DIAG_MODULES, draw_blockdiag
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from bridger.settings import bridger_settings

from .models import Asset
from .template import render_template_for_templatetag


class BlockDiag(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        try:
            blockdiag = request.data["markdown"]
            svg = draw_blockdiag(blockdiag, output_fmt="svg", font_antialias=True)
        except (ParseException, KeyError):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(svg)


class TemplateTagView(APIView):
    permission_classes = []

    def post(self, request: Request) -> Response:
        if templatetag := request.data.get("templatetag"):
            try:
                return Response(render_template_for_templatetag(templatetag, request=request))
            except exceptions.TemplateSyntaxError:
                return Response("malformatted templatetag", status=400)
            except Exception as e:
                return Response("not handled exception", status=400)
        return Response("templatetag missing", status=400)


class AssetCreateView(APIView):
    permission_classes = []

    def post(self, request: Request) -> Response:
        try:
            asset = Asset.objects.create(file=request.data["file"])
            return Response(reverse("bridger:asset-retrieve", args=[asset.id], request=request))
        except KeyError:
            return Response("file missing", status=400)


class AssetRetrieveView(APIView):
    permission_classes = []

    def get(self, request: Request, uuid: str) -> Response:
        try:
            asset = Asset.objects.get(id=uuid)
            response = HttpResponse(asset.file, content_type=asset.content_type)
            response["Content-Disposition"] = f"attachment; filename={asset.file_url_name}"
            return response
        except Asset.DoesNotExist:
            return Response(status=404)
        except ValidationError as e:
            return Response(*e, status=400)
