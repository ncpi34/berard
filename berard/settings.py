"""
Django settings for berard project.

Generated by 'django-admin startproject' using Django 2.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from django.contrib.messages import constants as messages
import environ
from django.utils.translation import ugettext_lazy as _
from dotenv import load_dotenv
# celery imports
from celery.schedules import crontab
import berard.tasks

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, 'berard/.env'))

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG')
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS")

DATABASES = {
    'default': {
        'ENGINE': os.getenv("DB_ENGINE"),
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PWD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    }
}

FIRST_CONNECTION = False
# MATERIAL_ADMIN_SITE = {
#     'HEADER':  _('Demo'),
#     'TITLE':  _('Demo'),
#     'FAVICON':  'demo.png',
#     'MAIN_BG_COLOR':  'green',
#     'MAIN_HOVER_COLOR':  'black',
#     'PROFILE_PICTURE':  'profile-background.jpeg',
#     'PROFILE_BG':  'profile-background.jpeg',
#     'LOGIN_LOGO':  'profile-background.jpeg',
#     'LOGOUT_BG':  'profile-background.jpeg',
#     'SHOW_THEMES':  True,
#     'TRAY_REVERSE': True,
#     'NAVBAR_REVERSE': True,
#     'SHOW_COUNTS': False,
#     'APP_ICONS': {
#         'invitations': 'send',
#     },
#     'MODEL_ICONS': {
#         'invitation': 'contact_mail',
#     }
# }

# Application definition

INSTALLED_APPS = [
    # 'material.admin',
    # 'material.admin.default',

    # 'celery',
    # 'django_celery_results',
    # 'django_celery_beat',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'bootstrap_modal_forms',
    'crispy_forms',
    'django_filters',
    'widget_tweaks',

    'website',
    'cart',
    'file_integration',
    'order',
]

CART_SESSION_ID = 'cart'  # during 15 days

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware'  # in case of 404 send email
    # 'django.middleware.locale.LocaleMiddleware', # i18n
]

ROOT_URLCONF = 'berard.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # add directory templates
            # os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'cart.context_processors.cart',  # cart processor
                'website.menus.get_menus',  # sidenav processor
                # "django.template.context_processors.i18n"  # i18n
            ],
        },
    },
]

WSGI_APPLICATION = 'berard.wsgi.application'

"""Password validation"""
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

"""Internationalization"""
LANGUAGE_CODE = 'fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True

""" Crispy """
CRISPY_TEMPLATE_PACK = 'bootstrap4'

""" StaticFiles """
STATIC_URL = '/static/'  # path admin statics
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # path to save (public)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATICFILES_DIRS = (
    # os.path.join(BASE_DIR + 'static_root'),  # path  not admin statics
    os.path.join(BASE_DIR + '/website/staticfiles'),  # path  not admin statics
)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

""" FlashMessages """
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-info',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

""" Email config """
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "/resources/sent_emails")
EMAIL_PORT = 587

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')

""" Caches """
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'cache_crepes'
    }
}

""" Celery """
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
# CELERY_BROKER_URL = 'amqp://localhost'
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Paris'

""" Email in case of problems """
ADMINS = (
    ('Le Dain Alexis', 'ledain.alexis@gmail.com'),
)
MANAGERS = ADMINS

"""Ftp address"""
# '213.215.12.22'
BERARD_FTP_HOST = os.getenv("BERARD_FTP_HOST")
BERARD_FTP_USER = os.getenv("BERARD_FTP_USER")
BERARD_FTP_PWD = os.getenv("BERARD_FTP_PWD")
