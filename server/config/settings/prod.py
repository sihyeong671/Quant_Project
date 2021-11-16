from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


sentry_sdk.init(
    dsn=env.str("SENTRY_SDK_dsn"),
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

def read_secret(secret_name):
    
    file = open('/run/secrets/' + secret_name)
    secret = file.read()
    secret = secret.strip()
    file.close()

    return secret


# 실제 배포시 바꿀 예정 -> False
DEBUG = False

ALLOWED_HOSTS = ['quant.or.kr', env.str("AWS_HOST")]

BASE_BACKEND_URL = env.str('DJANGO_BASE_BACKEND_URL')
BASE_FRONTEND_URL = env.str('DJANGO_BASE_FRONTEND_URL')


# CORS SETTINGS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = env.list(
    'DJANGO_CORS_ORIGIN_WHITELIST',
    default=[BASE_FRONTEND_URL]
)

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

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
