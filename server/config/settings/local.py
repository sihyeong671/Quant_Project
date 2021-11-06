from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

BASE_BACKEND_URL = 'http://localhost:8000'
BASE_FRONTEND_URL = 'http://localhost:3000'

INTERNAL_IPS = [
    '127.0.0.1',
]

# CORS SETTINGS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = env.list(
    'DJANGO_CORS_ORIGIN_WHITELIST',
    default=[BASE_FRONTEND_URL]
)

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DATA_UPLOAD_MAX_NUMBER_FIELDS = 20000
