import os
import sys

# Add project to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# Apply Django 1.11 Python 3.8+ compatibility patch
import django_patch

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "microfinance.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
