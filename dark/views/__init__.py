from django.apps import AppConfig


class DarkViewsConfig(AppConfig):
    name = 'dark.views'

    def ready(self):
        pass


default_app_config = 'dark.views.DarkViewsConfig'
