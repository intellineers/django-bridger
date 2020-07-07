from typing import Dict

import requests
from django.utils.html import strip_tags
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse

from bridger import display as dp
from bridger import serializers
from bridger.enums import Button, Operator, Unit, WBIcon
from bridger.settings import bridger_settings
from bridger.viewsets import ViewSet

story_type_choices = (("bug", "Bug"), ("feature", "Feature"))


def config(request: Request) -> Dict:
    return {
        "endpoint": reverse("bridger:clubhouse-list", request=request),
        "add": reverse("bridger:clubhouse-list", request=request),
    }


class ClubhouseSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyField()
    name = serializers.CharField(label="Name")
    story_type = serializers.ChoiceField(label="Type", choices=story_type_choices)
    description = serializers.MarkdownTextField(required=False)
    created_at = serializers.DateTimeField(read_only=True)
    completed = serializers.BooleanField(read_only=True)

    def validate(self, data):
        data["name"] = strip_tags(data["name"])
        description = f"**Reported by: {self.context['request'].user.username}**\n\n{data['description']}"
        data["description"] = description

        return data

    def create(self, validated_data):
        assert bridger_settings.CLUBHOUSE_API_TOKEN
        assert bridger_settings.CLUBHOUSE_PROJECT_ID

        response = requests.post(
            f"https://api.clubhouse.io/api/v3/stories?token={bridger_settings.CLUBHOUSE_API_TOKEN}",
            json={**validated_data, "project_id": bridger_settings.CLUBHOUSE_PROJECT_ID,},
            headers={"Content-Type": "application/json"},
        )

        return self.__class__(response.json())


class ClubHouseView(ViewSet):
    IDENTIFIER = "clubhouse"
    LIST_ENDPOINT = "bridger:clubhouse-list"
    INSTANCE_ENDPOINT = "bridger:clubhouse-list"
    CREATE_ENDPOINT = "bridger:clubhouse-list"

    LIST_TITLE = "Bug Reports"
    INSTANCE_TITLE = "Bug Report"

    BUTTONS = [Button.REFRESH.value, Button.NEW.value]
    CREATE_BUTTONS = [Button.SAVE.value]

    INSTANCE_DISPLAY = dp.InstanceDisplay(sections=[dp.Section(fields=dp.FieldSet(["name", "story_type", "description"]))])

    LIST_DISPLAY = dp.ListDisplay(
        fields=[
            dp.Field(key="id", label="Identifier", width=Unit.FRACTION(1)),
            dp.Field(key="created_at", label="Created", width=Unit.FRACTION(1)),
            dp.Field(key="name", label="Name", width=Unit.FRACTION(8)),
        ],
        formatting=[
            dp.Formatting(
                column="story_type",
                formatting_rules=[
                    dp.FormattingRule(icon=WBIcon.BOLD.value, condition=dp.Condition(operator=Operator.EQUAL, value="bug"),),
                    dp.FormattingRule(
                        icon=WBIcon.DATA.value, condition=dp.Condition(operator=Operator.EQUAL, value="feature"),
                    ),
                ],
            ),
            dp.Formatting(
                column="completed",
                formatting_rules=[
                    dp.FormattingRule(style={"backgroundColor": "#228B22"}, condition=dp.Condition(Operator.EQUAL, value=True),)
                ],
            ),
        ],
        legends=[
            dp.Legend(
                items=[
                    dp.LegendItem(icon=WBIcon.BOLD.value, label="Bug"),
                    dp.LegendItem(icon=WBIcon.DATA.value, label="Feature"),
                ]
            )
        ],
    )

    serializer_class = ClubhouseSerializer

    # We need to add this otherwise DjangoModelPermissions complains it cannot find a get_queryset method
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        clubhouse_story = serializer.save()
        return Response({"instance": clubhouse_story.data}, status=201)

    def retrieve(self, request, pk=None):
        assert bridger_settings.CLUBHOUSE_API_TOKEN

        response = requests.get(
            f"https://api.clubhouse.io/api/v3/stories/{pk}?token={bridger_settings.CLUBHOUSE_API_TOKEN}",
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 404:
            return Response({}, status=404)
        json_response = response.json()
        serializer = self.serializer_class(json_response)
        return Response({"instance": serializer.data})

    def list(self, request):
        assert bridger_settings.CLUBHOUSE_API_TOKEN
        assert bridger_settings.CLUBHOUSE_PROJECT_ID

        response = requests.get(
            f"https://api.clubhouse.io/api/v3/projects/{bridger_settings.CLUBHOUSE_PROJECT_ID}/stories?token={bridger_settings.CLUBHOUSE_API_TOKEN}",
            headers={"Content-Type": "application/json"},
        )
        json_response = response.json()

        serializer = self.serializer_class(json_response, many=True)
        return Response({"results": serializer.data})
