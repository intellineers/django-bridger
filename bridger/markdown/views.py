from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import status

from markdown_blockdiag.utils import draw_blockdiag, DIAG_MODULES
from blockdiag.parser import ParseException


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
