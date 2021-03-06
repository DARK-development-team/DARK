from pathlib import Path
import os

import django.conf.global_settings

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_h)u(6buzc2kk6^(svrf(c0d7^xaous&f_8yv&l#ekp4u=3_xg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    '0.0.0.0',
    'darkplatform.herokuapp.com',
    '127.0.0.1'
]

ROOT_URLCONF = 'dark.root_urls'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'dark/data/'),
]


WSGI_APPLICATION = 'base.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

LOGIN_REDIRECT_URL = 'home:page'
LOGOUT_REDIRECT_URL = 'home:page'

DEFAULT_FROM_EMAIL = "dark.io.project@gmail.com"
EMAIL_HOST_USER = "dark.io.project@gmail.com"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_PASSWORD = "SuperSecretPassword"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
