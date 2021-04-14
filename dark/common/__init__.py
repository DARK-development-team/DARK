from django.apps import AppConfig


class DarkCommonConfig(AppConfig):
    name = 'dark.common'

    def ready(self):
        pass


default_app_config = 'dark.common.DarkCommonConfig'
