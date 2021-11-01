from .base import *


def read_secret(secret_name):
    
    file = open('/run/secrets/' + secret_name)
    secret = file.read()
    secret = secret.strip()
    file.close()

    return secret

# 실제 배포시 바꿀 예정 -> False
DEBUG = True


BASE_BACKEND_URL = env.str('DJANGO_BASE_BACKEND_URL')
BASE_FRONTEND_URL = env.str('DJANGO_BASE_FRONTEND_URL')


# CORS SETTINGS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = env.list(
    'DJANGO_CORS_ORIGIN_WHITELIST',
    default=[BASE_FRONTEND_URL]
)

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'quantdb',
        'USER': 'quant',
        'PASSWORD': read_secret('QUANT_POSTGRES_PASSWORD'),
        'HOST': 'quantpostgres',
        'PORT': '5432',
    }
}
