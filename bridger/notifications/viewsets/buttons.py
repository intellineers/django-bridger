from bridger import buttons as bt
from bridger import display as dp
from bridger.buttons.enums import ButtonLevel
from bridger.utils.icons import WBIcon
from bridger.enums import RequestType
from bridger.buttons.metadata_config import ButtonConfig
from rest_framework.reverse import reverse

class NotificationButtonConfig(ButtonConfig):   
    def get_custom_instance_buttons(self):
        return {
            bt.ActionButton(
                method=RequestType.POST,
                action_label="All notifications read.",
                endpoint=reverse("bridger:notification-mark-all-as-read", request=self.request),
                description_fields="Do you want to mark notifications as read?",
                label="Mark all as read",
                icon=WBIcon.EYE.value,
                confirm_config=bt.ButtonConfig(label="Read all"),
                cancel_config=bt.ButtonConfig(label="Cancel"),
                identifiers=("relatedmodeltest-list",),
            ),
            bt.ActionButton(
                method=RequestType.POST,
                action_label="Delete all read notifications.",
                endpoint=reverse("bridger:notification-delete-all-read", request=self.request),
                description_fields="Do you want delete all read notifications?",
                label="Delete all read notifications",
                icon=WBIcon.TRASH.value,
                confirm_config=bt.ButtonConfig(label="Delete all", level=bt.ButtonLevel.WARNING),
                cancel_config=bt.ButtonConfig(label="Cancel", level=bt.ButtonLevel.ERROR),
                identifiers=(reverse("bridger:notification-list", request=self.request),),
            ),
        }
    def get_custom_list_instance_buttons(self):
        return self.get_custom_instance_buttons()