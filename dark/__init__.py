from django.apps import AppConfig


class DarkConfig(AppConfig):
    name = 'dark'

    def ready(self):
        pass


default_app_config = 'dark.DarkConfig'
