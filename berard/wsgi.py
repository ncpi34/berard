"""
WSGI config for berard project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""
import os
from django.core.wsgi import get_wsgi_application
import sys

from django.contrib.staticfiles.handlers import StaticFilesHandler
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'berard.settings')

application = get_wsgi_application()

path = '/testsite.uno'

if path not in sys.path:
    sys.path.append(path)


