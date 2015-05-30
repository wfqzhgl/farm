#-*-coding:utf-8-*-
"""
Django settings for farm project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import redis
import os
from loggers import *

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=)&g8e(96af^qx1c$bcvyzon-=hjhkr21a5$!3w)#lh++0161p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gunicorn',
    'public',
    'apps'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'farm.urls'

WSGI_APPLICATION = 'farm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
    'default': {
        'ENGINE': 'django.db.backends.mysql',

        'NAME': "farm",
        "USER": "farm",
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '',

    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-CN'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

MEDIA_URL = 'http://121.42.43.55:81/media/'

STATIC_URL = '/static/'
STATIC_ROOT = '/web/farm/static/'

CLIENT_XXTEA_KEY_PREFIX = "a90ksdf3609ec3c97c59"
REDIS_CLIENT = redis.Redis(host="127.0.0.1", port=6379)

##cache key
#hashkey for uid Token
HASHKEY_APPS_USER_TOKEN='hashkey_apps_user_token'

#默认每页行数
ROWS_DEFAULT = 30
#token header key
VEG_SESSION_HEADER_KEY = "HTTP_VEGSESSION"