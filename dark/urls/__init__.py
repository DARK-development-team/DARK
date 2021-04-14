from django.apps import AppConfig


class DarkUrlsConfig(AppConfig):
    name = 'dark.urls'

    def ready(self):
        pass


default_app_config = 'dark.urls.DarkUrlsConfig'
