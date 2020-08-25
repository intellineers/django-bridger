from bridger.titles.metadata_config import TitleConfig

class NotificationTitleConfig(TitleConfig):
    def get_instance_title(self):
        return "Notification: {{title}}"
    def get_list_title(self):
        return "Notifications"