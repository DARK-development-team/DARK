from django.apps import AppConfig


class HomeConfig(AppConfig):
    name = 'dark.home'


default_app_config = 'dark.home.HomeConfig'
