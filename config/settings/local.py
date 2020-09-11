from .base import *

SECRET_KEY = 's_76qvy1()h7jm@(fseey%92pk_6lqelwp)d1@2j7kttz6_#g9'
DEBUG = True
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "54.191.199.19"]
CORS_ORIGIN_ALLOW_ALL = True

MEDIA_URL = '/api/media/'
MEDIA_ROOT = BASE_DIR / 'media'

INSTALLED_APPS += ["django_extensions"]
