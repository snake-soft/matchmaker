"""
WSGI config for ranker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from config.settings import production

os.environ.setdefault("DJANGO_SETTINGS_MODULE", production)
# "config.settings.production"
application = get_wsgi_application()
