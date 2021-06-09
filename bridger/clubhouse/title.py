from bridger.titles.metadata_config import TitleConfig

class ClubHouseTitleConfig(TitleConfig):
    def get_instance_title(self):
        return "Bug Report"
    def get_list_title(self):
        return "Bug Reports"
    def get_create_title(self):
        return "New Report"
    def get_delete_title(self):
        return "Delete Report"
