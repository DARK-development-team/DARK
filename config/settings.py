import os

from split_settings.tools import optional, include
from django.contrib.messages import constants as messages

include(
    'options.py',
    'subsettings/installed_apps.py',
    'subsettings/auth_password_validators.py',
    'subsettings/databases.py',
    'subsettings/middleware.py',
    'subsettings/templates.py',
)


if 'HEROKU' in os.environ:
    import django_heroku
    django_heroku.settings(locals())

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

ALLOWED_HOSTS = [
    '0.0.0.0',
    'darkplatform.herokuapp.com',
    '127.0.0.1'
]
