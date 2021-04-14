from split_settings.tools import optional, include


include(
    'options.py',
    'subsettings/installed_apps.py',
    'subsettings/auth_password_validators.py',
    'subsettings/databases.py',
    'subsettings/middleware.py',
    'subsettings/templates.py',
)