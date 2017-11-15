"""
WSGI config for sp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sp.settings")

sys.path.append('/var/www/platform/students-platform')
sys.path.append('/var/www/platform/students-platform/sp/wsgi.py')

application = get_wsgi_application()
