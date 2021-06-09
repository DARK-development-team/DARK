from django.apps import AppConfig


class DarkFormsConfig(AppConfig):
    name = 'dark.forms'

    def ready(self):
        pass


default_app_config = 'dark.forms.DarkFormsConfig'
