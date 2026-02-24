import os
import sys

# Apply Django 1.11 Python 3.8+ compatibility patch
import django_patch

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise


PROJECT_DIR = os.path.abspath(__file__)
sys.path.append(PROJECT_DIR)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "microfinance.settings_local")

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
