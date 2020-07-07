from rest_framework.reverse import reverse

from bridger.buttons import ActionButton, ButtonConfig
from bridger.display import FieldSet, InstanceDisplay, Section
from bridger.enums import WBIcon
from bridger.settings import bridger_settings


def share_action_button(request):
    serializer = bridger_settings.DEFAULT_SHARE_SERIALIZER
    fields = [field for field in serializer().fields]

    btn = ActionButton(
        icon=WBIcon.TRADE.value,
        description_fields="",
        endpoint=reverse("bridger:share", request=request),
        instance_display=InstanceDisplay(sections=[Section(fields=FieldSet(fields=fields))]),
        confirm_config=ButtonConfig(label="Share", icon=WBIcon.TRADE.value),
        serializer=serializer,
    )
    btn.request = request
    return btn
