"""
WSGI config for fuelapp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fuelapp.settings")

application = get_wsgi_application()

# We included this to bridge the connection and connect to vercel
# we had set allowed hosts to be .vercel.app = hence app is important
# app = application
