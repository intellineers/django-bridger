from bridger.titles.metadata_config import TitleConfig

class ModelTestTitleConfig(TitleConfig):

    def get_instance_title(self):
        return "{{char_field}}"